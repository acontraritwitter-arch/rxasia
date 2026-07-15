#!/usr/bin/env python3
"""Playwright scrapers for Booking.com + TripAdvisor reviews.

Booking: warm session → open reviews → GraphQL ReviewList pagination (skip/limit).
TripAdvisor: page orN pagination with DOM extract.

Examples:
  pip install -r scripts/requirements-scraping.txt
  python3 -m playwright install chromium

  python3 scripts/scrape_booking_tripadvisor_playwright.py booking --max-pages 250
  python3 scripts/scrape_booking_tripadvisor_playwright.py tripadvisor --max-pages 50
  python3 scripts/scrape_booking_tripadvisor_playwright.py both --max-pages 250
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OUT_DIR = Path("data/onlinetours/jaz-casa-del-mar-beach")
HOTEL_NAME = "Jaz Elite Casa Del Mar Beach"
CORPUS_JSON = OUT_DIR / "reviews.all_sources.json"
CORPUS_MD = OUT_DIR / "REVIEWS_ALL.md"

BOOKING_PAGENAME = os.getenv("BOOKING_PAGENAME", "grand-plaza")
BOOKING_HOTEL_URL = (
    f"https://www.booking.com/hotel/eg/{BOOKING_PAGENAME}.en-gb.html"
)
BOOKING_HOTEL_ID = int(os.getenv("BOOKING_HOTEL_ID", "314504"))
BOOKING_UFI = int(os.getenv("BOOKING_UFI", "-290029"))
BOOKING_GQL = "https://www.booking.com/dml/graphql"
REVIEWLIST_QUERY = (
    Path(__file__).with_name("booking_reviewlist.graphql").read_text(encoding="utf-8")
)

TA_GEO = os.getenv("TA_GEO", "g297549")
TA_DETAIL = os.getenv("TA_DETAIL", "d23263857")
TA_SLUG = "JAZ_Elite_Casa_Del_Mar_Beach-Hurghada_Red_Sea_and_Sinai"


def ta_page_url(page_idx: int) -> str:
    or_token = "" if page_idx == 0 else f"or{page_idx * 5}-"
    return (
        f"https://www.tripadvisor.co.uk/Hotel_Review-{TA_GEO}-{TA_DETAIL}"
        f"-Reviews-{or_token}{TA_SLUG}.html"
    )


def _proxy_from_env(cli_proxy: str | None) -> dict[str, str] | None:
    raw = (cli_proxy or os.getenv("RESIDENTIAL_PROXY") or "").strip()
    if not raw:
        return None
    m = re.match(
        r"^(?P<scheme>https?|socks5)://(?:(?P<user>[^:@]+):(?P<pw>[^@]+)@)?"
        r"(?P<host>[^:/]+):(?P<port>\d+)/?$",
        raw,
    )
    if not m:
        raise SystemExit(f"Bad proxy format: {raw}")
    conf: dict[str, str] = {
        "server": f"{m.group('scheme')}://{m.group('host')}:{m.group('port')}"
    }
    if m.group("user"):
        conf["username"] = m.group("user")
        conf["password"] = m.group("pw")
    return conf


async def _new_context(
    playwright: Any,
    *,
    headed: bool,
    proxy: dict[str, str] | None,
    storage_state: Path | None,
    locale: str,
):
    browser = await playwright.chromium.launch(
        headless=not headed,
        proxy=proxy,
        args=["--disable-blink-features=AutomationControlled"],
    )
    kwargs: dict[str, Any] = {
        "locale": locale,
        "viewport": {"width": 1440, "height": 1100},
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
    }
    if storage_state and storage_state.exists():
        kwargs["storage_state"] = str(storage_state)
    context = await browser.new_context(**kwargs)
    await context.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
    )
    return browser, context


async def _human_pause(lo: float = 0.4, hi: float = 1.2) -> None:
    await asyncio.sleep(random.uniform(lo, hi))


async def _accept_cookies(page: Any) -> None:
    for sel in [
        "#onetrust-accept-btn-handler",
        "button#onetrust-accept-btn-handler",
        "button:has-text('Accept all')",
        "button:has-text('Accept')",
    ]:
        try:
            btn = page.locator(sel).first
            if await btn.count() and await btn.is_visible(timeout=1200):
                await btn.click(timeout=3000)
                await _human_pause(0.3, 0.8)
                return
        except Exception:
            continue


async def _wait_for_challenge(page: Any, headed: bool, label: str) -> bool:
    content = (await page.content()).lower()
    markers = (
        "not a robot",
        "captcha",
        "access denied",
        "please wait",
        "verify you are human",
        "cf-challenge",
    )
    blocked = any(m in content for m in markers)
    if blocked:
        print(f"[{label}] challenge detected", flush=True)
        if headed:
            print(f"[{label}] Solve captcha, then press Enter…", flush=True)
            await asyncio.to_thread(sys.stdin.readline)
            return False
        return True
    return False


def _ts_to_date(ts: int | None) -> str | None:
    if not ts:
        return None
    try:
        return datetime.fromtimestamp(int(ts), tz=timezone.utc).date().isoformat()
    except Exception:
        return None


def normalize_booking_card(card: dict[str, Any]) -> dict[str, Any] | None:
    guest = card.get("guestDetails") or {}
    text = card.get("textDetails") or {}
    booking = card.get("bookingDetails") or {}
    room = (booking.get("roomType") or {}).get("name")
    parts: list[str] = []
    if text.get("title"):
        parts.append(str(text["title"]))
    if text.get("positiveText"):
        parts.append(f"Плюсы: {text['positiveText']}")
    if text.get("negativeText"):
        parts.append(f"Минусы: {text['negativeText']}")
    body = "\n\n".join(parts).strip()
    if len(body) < 5:
        return None
    author = None if guest.get("anonymous") else guest.get("username")
    return {
        "source": "booking.com",
        "source_url": BOOKING_HOTEL_URL,
        "id": card.get("reviewUrl"),
        "author": author,
        "title": text.get("title"),
        "rating": card.get("reviewScore"),
        "published_at": _ts_to_date(card.get("reviewedDate")),
        "visit_date": booking.get("checkinDate"),
        "group_type": guest.get("guestTypeTranslation") or booking.get("customerType"),
        "room_type": room,
        "nights": booking.get("numNights"),
        "country": guest.get("countryName"),
        "lang": text.get("lang"),
        "text": body,
        "partner_reply": ((card.get("partnerReply") or {}).get("reply")),
    }


# ---------------------------------------------------------------------------
# Booking via GraphQL
# ---------------------------------------------------------------------------

async def scrape_booking(
    *,
    headed: bool,
    proxy: dict[str, str] | None,
    storage_state: Path | None,
    max_pages: int,
    rows: int = 10,
    save_storage: Path | None,
) -> list[dict[str, Any]]:
    try:
        from playwright.async_api import async_playwright
    except ImportError as exc:
        raise SystemExit(
            "Install: pip install -r scripts/requirements-scraping.txt "
            "&& python3 -m playwright install chromium"
        ) from exc

    reviews: list[dict[str, Any]] = []
    async with async_playwright() as p:
        browser, context = await _new_context(
            p,
            headed=headed,
            proxy=proxy,
            storage_state=storage_state,
            locale="en-GB",
        )
        page = await context.new_page()
        print(f"[Booking] open {BOOKING_HOTEL_URL}", flush=True)
        await page.goto(BOOKING_HOTEL_URL, wait_until="domcontentloaded", timeout=90000)
        await _human_pause(1.0, 2.0)
        await _accept_cookies(page)
        if await _wait_for_challenge(page, headed, "Booking"):
            await browser.close()
            return reviews

        # Open reviews list so GraphQL/session is primed
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight * 0.35)")
        await _human_pause(0.8, 1.5)
        opened = False
        for sel in [
            '[data-testid="review-score-read-all"]',
            '[data-testid="fr-read-all-reviews"]',
            '[data-testid="Property-Header-Nav-Tab-Trigger-reviews"]',
            "button:has-text('Read all reviews')",
            "span:has-text('Read all reviews')",
        ]:
            loc = page.locator(sel).first
            try:
                if await loc.count():
                    await loc.scroll_into_view_if_needed()
                    await loc.click(timeout=5000)
                    opened = True
                    print(f"[Booking] opened reviews via {sel}", flush=True)
                    break
            except Exception:
                continue
        if not opened:
            print("[Booking] could not open reviews UI", flush=True)
        await page.wait_for_timeout(2500)

        skip = 0
        page_idx = 0
        empty_streak = 0
        while page_idx < max_pages:
            payload = {
                "operationName": "ReviewList",
                "variables": {
                    "shouldShowReviewListPhotoAltText": True,
                    "shouldGetUserReviewCount": False,
                    "input": {
                        "hotelId": BOOKING_HOTEL_ID,
                        "ufi": BOOKING_UFI,
                        "hotelCountryCode": "eg",
                        "sorter": "NEWEST_FIRST",
                        "filters": {"text": ""},
                        "skip": skip,
                        "limit": rows,
                        "hotelScore": 9.2,
                        "upsortReviewUrl": "",
                        "searchFeatures": {
                            "destId": BOOKING_UFI,
                            "destType": "CITY",
                        },
                    },
                },
                "query": REVIEWLIST_QUERY,
                "extensions": {},
            }

            result = await page.evaluate(
                """async ({url, payload}) => {
                  const res = await fetch(url, {
                    method: 'POST',
                    credentials: 'include',
                    headers: { 'content-type': 'application/json' },
                    body: JSON.stringify(payload),
                  });
                  const text = await res.text();
                  return { status: res.status, text };
                }""",
                {"url": BOOKING_GQL, "payload": payload},
            )
            if result["status"] != 200:
                print(
                    f"[Booking] GraphQL HTTP {result['status']} at skip={skip}",
                    flush=True,
                )
                dump = OUT_DIR / f"debug_booking_gql_{skip}.txt"
                dump.write_text(result["text"][:5000], encoding="utf-8")
                break
            try:
                data = json.loads(result["text"])
            except json.JSONDecodeError:
                print(f"[Booking] bad JSON at skip={skip}", flush=True)
                break

            rlf = ((data.get("data") or {}).get("reviewListFrontend")) or {}
            if rlf.get("__typename") == "ReviewsFrontendError":
                print(f"[Booking] API error: {rlf}", flush=True)
                break
            cards = rlf.get("reviewCard") or []
            total = rlf.get("reviewsCount")
            if not cards:
                empty_streak += 1
                print(f"[Booking] empty at skip={skip} total={total}", flush=True)
                if empty_streak >= 2:
                    break
            else:
                empty_streak = 0
                added = 0
                for card in cards:
                    item = normalize_booking_card(card)
                    if item:
                        reviews.append(item)
                        added += 1
                print(
                    f"[Booking] skip={skip}: +{added}/{len(cards)} "
                    f"(run={len(reviews)} total={total})",
                    flush=True,
                )
                if total and skip + len(cards) >= int(total):
                    break

            skip += rows
            page_idx += 1
            await _human_pause(0.35, 0.9)

        if save_storage:
            await context.storage_state(path=str(save_storage))
            print(f"[Booking] storage → {save_storage}", flush=True)
        await browser.close()

    return _dedup_reviews(reviews)


# ---------------------------------------------------------------------------
# TripAdvisor
# ---------------------------------------------------------------------------

async def scrape_tripadvisor(
    *,
    headed: bool,
    proxy: dict[str, str] | None,
    storage_state: Path | None,
    max_pages: int,
    save_storage: Path | None,
) -> list[dict[str, Any]]:
    try:
        from playwright.async_api import async_playwright
    except ImportError as exc:
        raise SystemExit(
            "Install: pip install -r scripts/requirements-scraping.txt "
            "&& python3 -m playwright install chromium"
        ) from exc

    reviews: list[dict[str, Any]] = []
    async with async_playwright() as p:
        browser, context = await _new_context(
            p,
            headed=headed,
            proxy=proxy,
            storage_state=storage_state,
            locale="en-GB",
        )
        page = await context.new_page()

        for page_idx in range(max_pages):
            url = ta_page_url(page_idx)
            print(f"[TripAdvisor] page={page_idx + 1} {url}", flush=True)
            await page.goto(url, wait_until="domcontentloaded", timeout=90000)
            await _human_pause(1.2, 2.5)
            if await _wait_for_challenge(page, headed, "TripAdvisor"):
                break

            for _ in range(10):
                more = page.locator("span:has-text('Read more'), a:has-text('Read more')").first
                try:
                    if await more.count() and await more.is_visible():
                        await more.click(timeout=1500)
                        await _human_pause(0.2, 0.5)
                    else:
                        break
                except Exception:
                    break

            items = await page.evaluate(
                """() => {
                  const out = [];
                  const cards = document.querySelectorAll(
                    '[data-test-target="HR_CC_CARD"], [data-reviewid], .review-container'
                  );
                  const pick = (el, sels) => {
                    for (const s of sels) {
                      const n = el.querySelector(s);
                      if (n && n.textContent.trim()) return n.textContent.trim();
                    }
                    return null;
                  };
                  for (const el of cards) {
                    const author = pick(el, [
                      '[data-test-target="reviews_member_name"] a',
                      'a[href*="/Profile/"]',
                      '.info_text div',
                    ]);
                    const title = pick(el, [
                      '[data-test-target="review-title"]',
                      'a[href*="ShowUserReviews"] span',
                      '.noQuotes',
                    ]);
                    const body = pick(el, [
                      '[data-test-target="review-content"]',
                      'q span',
                      '.partial_entry',
                    ]);
                    let rating = null;
                    const ratingEl = el.querySelector(
                      'svg[aria-label*="bubble"], span.ui_bubble_rating, [class*="bubble_"]'
                    );
                    if (ratingEl) {
                      const al = ratingEl.getAttribute('aria-label')
                        || ratingEl.getAttribute('class') || '';
                      const m = al.match(/(\\d)\\s*of\\s*5|bubble_(\\d0)/);
                      if (m) rating = m[1] ? Number(m[1]) : Number(m[2]) / 10;
                    }
                    const date = pick(el, [
                      '[data-test-target="review-date"]',
                      '.ratingDate',
                      'span:has-text("Date of stay")',
                    ]);
                    if ((body && body.length > 40) || title) {
                      out.push({ author, title, body, rating, date });
                    }
                  }
                  return out;
                }"""
            )

            if not items:
                dump = OUT_DIR / f"debug_ta_page_{page_idx}.html"
                dump.write_text(await page.content(), encoding="utf-8")
                print(f"[TripAdvisor] empty; saved {dump}", flush=True)
                # stop early if clearly blocked/empty
                if page_idx >= 2:
                    break
                continue

            before = len(reviews)
            for it in items:
                text = "\n\n".join(
                    x for x in [it.get("title"), it.get("body")] if x
                ).strip()
                if len(text) < 40:
                    continue
                reviews.append(
                    {
                        "source": "tripadvisor.co.uk",
                        "source_url": url,
                        "author": it.get("author"),
                        "title": it.get("title"),
                        "rating": it.get("rating"),
                        "published_at": it.get("date"),
                        "text": text,
                    }
                )
            print(
                f"[TripAdvisor] +{len(reviews) - before} "
                f"(unique {len(_dedup_reviews(reviews))})",
                flush=True,
            )
            await _human_pause(1.0, 2.2)

        if save_storage:
            await context.storage_state(path=str(save_storage))
        await browser.close()

    return _dedup_reviews(reviews)


# ---------------------------------------------------------------------------
# Corpus merge
# ---------------------------------------------------------------------------

def _dedup_reviews(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[Any, ...]] = set()
    out: list[dict[str, Any]] = []
    for r in items:
        key = (
            r.get("source"),
            r.get("id") or r.get("author"),
            (r.get("title") or ""),
            (r.get("text") or "")[:120],
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def fingerprint(r: dict[str, Any]) -> tuple[Any, ...]:
    if r.get("id") and r.get("source"):
        return (r.get("source"), r.get("id"))
    return (
        r.get("source"),
        r.get("author"),
        (r.get("title") or ""),
        (r.get("text") or "")[:160],
    )


def merge_into_corpus(new_items: list[dict[str, Any]]) -> dict[str, Any]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if CORPUS_JSON.exists():
        data = json.loads(CORPUS_JSON.read_text(encoding="utf-8"))
    else:
        data = {"hotel": HOTEL_NAME, "reviews": []}

    # Drop previously bad booking placeholder junk
    cleaned = []
    for r in data.get("reviews", []):
        if r.get("source") == "booking.com":
            t = r.get("text") or ""
            if "It starts with a booking" in t or "Followed by a trip" in t:
                continue
            if r.get("rating") is None and len(t) < 80:
                continue
        cleaned.append(r)
    data["reviews"] = cleaned

    existing = {fingerprint(r) for r in data["reviews"]}
    added = 0
    for r in new_items:
        fp = fingerprint(r)
        if fp in existing:
            continue
        data["reviews"].append(r)
        existing.add(fp)
        added += 1

    data["hotel"] = HOTEL_NAME
    data["collected_at"] = datetime.now(timezone.utc).isoformat()
    data["by_source"] = dict(Counter(r.get("source") for r in data["reviews"]))
    data["total"] = len(data["reviews"])
    CORPUS_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_markdown(data)
    print(
        json.dumps(
            {"added": added, "total": data["total"], "by_source": data["by_source"]},
            ensure_ascii=False,
            indent=2,
        )
    )
    return data


def write_markdown(data: dict[str, Any]) -> None:
    parts: list[str] = [
        f"# Отзывы об отеле {HOTEL_NAME}\n",
        "Максимально доступная выгрузка из открытых источников.\n",
        f"- Дата сбора: `{data.get('collected_at')}`\n",
        f"- Всего отзывов в файле: **{data.get('total')}**\n",
        "## Источники\n",
    ]
    for src, cnt in sorted(
        (data.get("by_source") or {}).items(), key=lambda x: -x[1]
    ):
        parts.append(f"- {src}: {cnt}\n")
    parts.append("\n---\n\n## Все отзывы\n\n")

    for i, r in enumerate(data.get("reviews") or [], 1):
        parts.append(f"### {i}. {r.get('author') or 'Без имени'}\n")
        meta = []
        if r.get("source"):
            meta.append(
                f"источник: [{r['source']}]({r.get('source_url') or '#'})"
            )
        if r.get("rating") is not None:
            meta.append(f"оценка: **{r['rating']}**")
        if r.get("published_at"):
            meta.append(f"опубликован: {r['published_at']}")
        if r.get("visit_date"):
            meta.append(f"визит: {r['visit_date']}")
        if r.get("visit_period"):
            meta.append(f"период: {r['visit_period']}")
        if r.get("group_type"):
            meta.append(f"компания: {r['group_type']}")
        if r.get("traveled_with"):
            meta.append(f"компания: {r['traveled_with']}")
        if r.get("room_type"):
            meta.append(f"номер: {r['room_type']}")
        if r.get("country"):
            meta.append(f"страна: {r['country']}")
        if r.get("confirmed_stay"):
            meta.append("проживание подтверждено")
        if meta:
            parts.append("- " + " · ".join(meta) + "\n")
        cats = r.get("category_ratings") or {}
        if cats:
            cat_s = ", ".join(
                f"{k}: {v}" for k, v in cats.items() if v is not None
            )
            if cat_s:
                parts.append(f"- категории: {cat_s}\n")
        if r.get("title"):
            parts.append(f"\n**{str(r['title']).strip()}**\n\n")
        text = str(r.get("text") or "").strip()
        if text:
            parts.append(text + "\n")
        parts.append("\n---\n\n")

    CORPUS_MD.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {CORPUS_MD} ({CORPUS_MD.stat().st_size} bytes)", flush=True)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "target",
        choices=["booking", "tripadvisor", "both", "merge-only"],
    )
    p.add_argument("--headed", action="store_true")
    p.add_argument("--proxy", default=None)
    p.add_argument("--storage-state", type=Path, default=None)
    p.add_argument("--save-storage", type=Path, default=None)
    p.add_argument("--max-pages", type=int, default=250)
    p.add_argument("--rows", type=int, default=10, help="Booking GraphQL page size")
    p.add_argument("--no-merge", action="store_true")
    return p


async def async_main(args: argparse.Namespace) -> None:
    proxy = _proxy_from_env(args.proxy)
    collected: list[dict[str, Any]] = []
    if args.target in {"booking", "both"}:
        collected += await scrape_booking(
            headed=args.headed,
            proxy=proxy,
            storage_state=args.storage_state,
            max_pages=args.max_pages,
            rows=args.rows,
            save_storage=args.save_storage,
        )
    if args.target in {"tripadvisor", "both"}:
        collected += await scrape_tripadvisor(
            headed=args.headed,
            proxy=proxy,
            storage_state=args.storage_state,
            max_pages=min(args.max_pages, 400),
            save_storage=args.save_storage,
        )
    collected = _dedup_reviews(collected)
    print(f"Collected {len(collected)} reviews this run", flush=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    run_path = OUT_DIR / f"playwright_run_{args.target}.json"
    run_path.write_text(
        json.dumps(collected, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Saved raw run → {run_path}", flush=True)
    if not args.no_merge:
        merge_into_corpus(collected)


def main() -> None:
    args = build_parser().parse_args()
    if args.target == "merge-only":
        data = json.loads(CORPUS_JSON.read_text(encoding="utf-8"))
        write_markdown(data)
        return
    asyncio.run(async_main(args))


if __name__ == "__main__":
    main()
