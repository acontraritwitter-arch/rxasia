#!/usr/bin/env python3
"""Playwright scrapers for Booking.com + TripAdvisor reviews.

Designed for ONE hotel at a time, with slow human-like pacing.
Does NOT solve captchas automatically — if a challenge appears, use
`--headed` and pass it manually, or load a saved `--storage-state`.

Examples:
  pip install -r scripts/requirements-scraping.txt
  playwright install chromium

  # Booking review list (paginated)
  python3 scripts/scrape_booking_tripadvisor_playwright.py booking \\
    --headed --max-pages 20

  # TripAdvisor orN pages
  python3 scripts/scrape_booking_tripadvisor_playwright.py tripadvisor \\
    --headed --max-pages 50

  # Both, then merge into REVIEWS_ALL.md
  python3 scripts/scrape_booking_tripadvisor_playwright.py both \\
    --headed --proxy "$RESIDENTIAL_PROXY" --storage-state ./storage.json

Env:
  RESIDENTIAL_PROXY   e.g. http://user:pass@host:port
  BOOKING_PAGENAME    default: grand-plaza
  TA_GEO / TA_DETAIL  default: g297549 / d23263857
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
from urllib.parse import quote

OUT_DIR = Path("data/onlinetours/jaz-casa-del-mar-beach")
HOTEL_NAME = "Jaz Elite Casa Del Mar Beach"
CORPUS_JSON = OUT_DIR / "reviews.all_sources.json"
CORPUS_MD = OUT_DIR / "REVIEWS_ALL.md"

BOOKING_PAGENAME = os.getenv("BOOKING_PAGENAME", "grand-plaza")
BOOKING_HOTEL_URL = (
    f"https://www.booking.com/hotel/eg/{BOOKING_PAGENAME}.en-gb.html"
)
BOOKING_REVIEWLIST = (
    "https://www.booking.com/reviewlist.en-gb.html"
    f"?cc1=eg;pagename={BOOKING_PAGENAME};type=total;"
    "sort=f_recent_desc;rows={rows};offset={offset}"
)

TA_GEO = os.getenv("TA_GEO", "g297549")
TA_DETAIL = os.getenv("TA_DETAIL", "d23263857")
TA_SLUG = "JAZ_Elite_Casa_Del_Mar_Beach-Hurghada_Red_Sea_and_Sinai"
def ta_page_url(page_idx: int) -> str:
    """TripAdvisor uses or5 / or10 / … offsets (5 reviews per page)."""
    or_token = "" if page_idx == 0 else f"or{page_idx * 5}-"
    return (
        f"https://www.tripadvisor.co.uk/Hotel_Review-{TA_GEO}-{TA_DETAIL}"
        f"-Reviews-{or_token}{TA_SLUG}.html"
    )


# ---------------------------------------------------------------------------
# Browser helpers
# ---------------------------------------------------------------------------

def _proxy_from_env(cli_proxy: str | None) -> dict[str, str] | None:
    raw = cli_proxy or os.getenv("RESIDENTIAL_PROXY") or ""
    raw = raw.strip()
    if not raw:
        return None
    # Playwright accepts server + optional username/password
    # Formats: http://user:pass@host:port  OR  http://host:port
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
        "viewport": {"width": 1365, "height": 900},
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
    }
    if storage_state and storage_state.exists():
        kwargs["storage_state"] = str(storage_state)
    context = await browser.new_context(**kwargs)
    # Light stealth: hide webdriver flag
    await context.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
    )
    return browser, context


async def _human_pause(lo: float = 0.8, hi: float = 2.2) -> None:
    await asyncio.sleep(random.uniform(lo, hi))


async def _wait_for_challenge(page: Any, headed: bool, label: str) -> bool:
    """Return True if page looks blocked/challenged."""
    content = (await page.content()).lower()
    markers = (
        "not a robot",
        "enable javascript",
        "captcha",
        "access denied",
        "please wait",
        "cf-challenge",
        "attention required",
        "verify you are human",
    )
    blocked = any(m in content for m in markers) or len(content) < 1500
    if blocked:
        print(f"[{label}] challenge/empty page detected", flush=True)
        if headed:
            print(
                f"[{label}] Solve captcha in the browser window, then press Enter here…",
                flush=True,
            )
            await asyncio.to_thread(sys.stdin.readline)
            return False
        return True
    return False


# ---------------------------------------------------------------------------
# Booking.com
# ---------------------------------------------------------------------------

async def scrape_booking(
    *,
    headed: bool,
    proxy: dict[str, str] | None,
    storage_state: Path | None,
    max_pages: int,
    rows: int = 25,
    save_storage: Path | None,
) -> list[dict[str, Any]]:
    try:
        from playwright.async_api import async_playwright
    except ImportError as exc:
        raise SystemExit(
            "Install: pip install -r scripts/requirements-scraping.txt "
            "&& playwright install chromium"
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

        # Warm-up: land on hotel page to get cookies
        print(f"[Booking] open {BOOKING_HOTEL_URL}", flush=True)
        await page.goto(BOOKING_HOTEL_URL, wait_until="domcontentloaded", timeout=90000)
        await _human_pause(1.5, 3.0)
        if await _wait_for_challenge(page, headed, "Booking"):
            await browser.close()
            return reviews

        # Accept cookies banner if present
        for sel in [
            "#onetrust-accept-btn-handler",
            "button#onetrust-accept-btn-handler",
            "button:has-text('Accept')",
            "button:has-text('Accept all')",
        ]:
            try:
                btn = page.locator(sel).first
                if await btn.count() and await btn.is_visible():
                    await btn.click(timeout=3000)
                    await _human_pause()
                    break
            except Exception:
                pass

        for page_idx in range(max_pages):
            offset = page_idx * rows
            url = BOOKING_REVIEWLIST.format(rows=rows, offset=offset)
            print(f"[Booking] offset={offset} {url}", flush=True)
            await page.goto(url, wait_until="domcontentloaded", timeout=90000)
            await _human_pause(1.0, 2.5)
            if await _wait_for_challenge(page, headed, "Booking"):
                break

            # reviewlist often returns fragment HTML with review blocks
            items = await page.evaluate(
                """() => {
                  const out = [];
                  const blocks = document.querySelectorAll(
                    '[data-testid="review-card"], .review_list_new_item_block, .review_item, .c-review-block'
                  );
                  const nodes = blocks.length ? blocks : [];
                  for (const el of nodes) {
                    const author =
                      el.querySelector('[data-testid="review-avatar"] + * , .bui-avatar-block__title, .reviewer_name')?.textContent?.trim()
                      || el.querySelector('.bui-avatar-block__title')?.textContent?.trim()
                      || null;
                    const score =
                      el.querySelector('[data-testid="review-score"] , .bui-review-score__badge, .review-score-badge')?.textContent?.trim()
                      || null;
                    const title =
                      el.querySelector('[data-testid="review-title"] , .c-review-block__title, .review_item_header_content_title')?.textContent?.trim()
                      || null;
                    const date =
                      el.querySelector('[data-testid="review-date"] , .c-review-block__date, .review_item_date')?.textContent?.trim()
                      || null;
                    const pros =
                      el.querySelector('[data-testid="review-positive"] , .c-review__quote, .review_pos')?.textContent?.trim()
                      || null;
                    const cons =
                      el.querySelector('[data-testid="review-negative"] , .review_neg')?.textContent?.trim()
                      || null;
                    const texts = [...el.querySelectorAll('.c-review__body, [data-testid="review-content"] , .review_item_review_content')]
                      .map(n => n.textContent.trim()).filter(Boolean);
                    const body = [pros && `Плюсы: ${pros}`, cons && `Минусы: ${cons}`, ...texts]
                      .filter(Boolean).join('\\n\\n');
                    if (body || title) {
                      out.push({ author, score, title, date, body });
                    }
                  }
                  // fallback: gather review-ish cards by score badge presence
                  if (!out.length) {
                    for (const el of document.querySelectorAll('.review_list_new_item_block, li')) {
                      const t = el.innerText || '';
                      if (t.length < 80) continue;
                      if (!/\\b\\d([.,]\\d)?\\b/.test(t)) continue;
                      out.push({
                        author: null,
                        score: null,
                        title: null,
                        date: null,
                        body: t.slice(0, 4000),
                      });
                    }
                  }
                  return out;
                }"""
            )

            if not items:
                html = await page.content()
                dump = OUT_DIR / f"debug_booking_offset_{offset}.html"
                dump.write_text(html, encoding="utf-8")
                print(
                    f"[Booking] no items at offset={offset}; saved {dump}",
                    flush=True,
                )
                break

            for it in items:
                text_parts = []
                if it.get("title"):
                    text_parts.append(it["title"])
                if it.get("body"):
                    text_parts.append(it["body"])
                text = "\n\n".join(text_parts).strip()
                if len(text) < 20:
                    continue
                score = it.get("score")
                try:
                    rating = float(str(score).replace(",", ".")) if score else None
                except ValueError:
                    rating = None
                reviews.append(
                    {
                        "source": "booking.com",
                        "source_url": BOOKING_HOTEL_URL,
                        "author": it.get("author"),
                        "title": it.get("title"),
                        "rating": rating,
                        "published_at": it.get("date"),
                        "text": text,
                    }
                )
            print(
                f"[Booking] page {page_idx + 1}: +{len(items)} "
                f"(unique corpus so far {len(reviews)})",
                flush=True,
            )
            await _human_pause(1.2, 3.0)

        if save_storage:
            await context.storage_state(path=str(save_storage))
            print(f"[Booking] saved storage state → {save_storage}", flush=True)
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
            "&& playwright install chromium"
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
            await _human_pause(1.5, 3.5)
            if await _wait_for_challenge(page, headed, "TripAdvisor"):
                break

            # Expand "Read more" where possible
            for _ in range(8):
                more = page.locator("text=Read more").first
                try:
                    if await more.count() and await more.is_visible():
                        await more.click(timeout=2000)
                        await _human_pause(0.3, 0.8)
                    else:
                        break
                except Exception:
                    break

            items = await page.evaluate(
                """() => {
                  const out = [];
                  // Modern TA cards
                  const cards = document.querySelectorAll(
                    '[data-test-target="HR_CC_CARD"], [data-reviewid], .review-container, .WAllg'
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
                      'a.ui_header_link',
                      '.info_text div',
                    ]);
                    const title = pick(el, [
                      '[data-test-target="review-title"]',
                      '.Qwuub a span',
                      '.noQuotes',
                    ]);
                    const body = pick(el, [
                      '[data-test-target="review-content"]',
                      '.Qwuub span',
                      '.partial_entry',
                      'q span',
                    ]);
                    const ratingEl = el.querySelector(
                      'svg[aria-label*="bubble"], span.ui_bubble_rating, [class*="bubble_"]'
                    );
                    let rating = null;
                    if (ratingEl) {
                      const al = ratingEl.getAttribute('aria-label')
                        || ratingEl.getAttribute('class')
                        || '';
                      const m = al.match(/(\\d)\\s*of\\s*5|bubble_(\\d0)/);
                      if (m) rating = m[1] ? Number(m[1]) : Number(m[2]) / 10;
                    }
                    const date = pick(el, [
                      '[data-test-target="review-date"]',
                      '.cRVSd span',
                      '.ratingDate',
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
                print(f"[TripAdvisor] empty page; saved {dump}", flush=True)
                break

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
            await _human_pause(1.5, 3.5)

        if save_storage:
            await context.storage_state(path=str(save_storage))
            print(f"[TripAdvisor] saved storage state → {save_storage}", flush=True)
        await browser.close()

    return _dedup_reviews(reviews)


# ---------------------------------------------------------------------------
# Merge into corpus + MD
# ---------------------------------------------------------------------------

def _dedup_reviews(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[Any, ...]] = set()
    out: list[dict[str, Any]] = []
    for r in items:
        key = (
            r.get("source"),
            r.get("author"),
            (r.get("title") or ""),
            (r.get("text") or "")[:120],
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def fingerprint(r: dict[str, Any]) -> tuple[Any, ...]:
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

    existing = {fingerprint(r) for r in data.get("reviews", [])}
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
    parts.append("\n## Покрытие и ограничения\n\n")
    parts.append(
        "- Booking/TripAdvisor: Playwright-скрипт "
        "`scripts/scrape_booking_tripadvisor_playwright.py` "
        "(headed / storage-state / residential proxy).\n"
    )
    parts.append(
        "- Без валидной браузерной сессии сайты отдают captcha/JS-challenge.\n\n"
    )
    parts.append("---\n\n## Все отзывы\n\n")

    for i, r in enumerate(data.get("reviews") or [], 1):
        parts.append(f"### {i}. {r.get('author') or 'Без имени'}\n")
        meta = []
        if r.get("source"):
            meta.append(
                f"источник: [{r['source']}]({r.get('source_url') or '#'})"
            )
        if r.get("rating") is not None:
            meta.append(f"оценка: **{r['rating']}**")
        if r.get("recommendation") is True:
            meta.append("рекомендует")
        if r.get("recommendation") is False:
            meta.append("не рекомендует")
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
        if r.get("locale"):
            meta.append(f"язык: {r['locale']}")
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


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "target",
        choices=["booking", "tripadvisor", "both", "merge-only"],
        help="Что скрейпить",
    )
    p.add_argument("--headed", action="store_true", help="Показать окно браузера")
    p.add_argument("--proxy", default=None, help="http://user:pass@host:port")
    p.add_argument(
        "--storage-state",
        type=Path,
        default=None,
        help="Путь к Playwright storage state (cookies)",
    )
    p.add_argument(
        "--save-storage",
        type=Path,
        default=None,
        help="Сохранить storage state после сессии",
    )
    p.add_argument("--max-pages", type=int, default=5, help="Сколько страниц/оффсетов")
    p.add_argument("--rows", type=int, default=25, help="Booking rows per page")
    p.add_argument(
        "--no-merge",
        action="store_true",
        help="Не мержить в REVIEWS_ALL.md (только вывести JSON в stdout)",
    )
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
            max_pages=args.max_pages,
            save_storage=args.save_storage,
        )

    collected = _dedup_reviews(collected)
    print(f"Collected {len(collected)} reviews this run", flush=True)

    # Persist raw run dump
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    run_path = OUT_DIR / f"playwright_run_{args.target}.json"
    run_path.write_text(
        json.dumps(collected, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Saved raw run → {run_path}", flush=True)

    if args.no_merge:
        print(json.dumps(collected, ensure_ascii=False, indent=2))
        return
    if args.target == "merge-only":
        # Remerge existing corpus into MD only
        if not CORPUS_JSON.exists():
            raise SystemExit(f"No corpus at {CORPUS_JSON}")
        data = json.loads(CORPUS_JSON.read_text(encoding="utf-8"))
        write_markdown(data)
        return
    merge_into_corpus(collected)


def main() -> None:
    args = build_parser().parse_args()
    if args.target == "merge-only":
        if not CORPUS_JSON.exists():
            raise SystemExit(f"No corpus at {CORPUS_JSON}")
        data = json.loads(CORPUS_JSON.read_text(encoding="utf-8"))
        write_markdown(data)
        return
    asyncio.run(async_main(args))


if __name__ == "__main__":
    main()
