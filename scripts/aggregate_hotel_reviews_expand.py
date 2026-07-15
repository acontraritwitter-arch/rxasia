#!/usr/bin/env python3
"""Expand review corpus: HolidayCheck pages + TopHotels retries + author fix."""

from __future__ import annotations

import concurrent.futures
import json
import re
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
OUT_DIR = Path("data/onlinetours/jaz-casa-del-mar-beach")
HOTEL_NAME = "Jaz Elite Casa Del Mar Beach"
HC_HOTEL = "12301882-937d-4fc9-bc48-cf242a76303e"
HC_SLUG = "bewertungen-jaz-elite-casa-del-mar-beach"


def fetch(url: str, timeout: int = 60) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept-Language": "de-CH,de;q=0.9,en;q=0.8,ru;q=0.7",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract_js_object(html: str, marker: str) -> dict[str, Any] | None:
    pos = html.find(marker)
    if pos < 0:
        return None
    p = pos + len(marker)
    if p >= len(html) or html[p] != "{":
        return None
    depth = 0
    in_str = False
    esc = False
    end = None
    for i, ch in enumerate(html[p:], p):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end is None:
        return None
    raw = re.sub(r"\bundefined\b", "null", html[p:end])
    raw = re.sub(r"\bNaN\b", "null", raw)
    return json.loads(raw)


def ms_to_date(ms: int | None) -> str | None:
    if not ms:
        return None
    try:
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).date().isoformat()
    except Exception:
        return None


def normalize_hc_item(item: dict[str, Any]) -> dict[str, Any]:
    parts: list[str] = []
    ratings: dict[str, Any] = {}
    for key, contrib in (item.get("contributions") or {}).items():
        if not isinstance(contrib, dict):
            continue
        if contrib.get("inputType") == "TEXT" and contrib.get("value"):
            label = contrib.get("text") or key
            parts.append(f"{label}: {contrib['value']}")
        elif contrib.get("inputType") == "RATING":
            val = contrib.get("value")
            if val is not None:
                ratings[contrib.get("text") or key] = val
    user = item.get("user") or {}
    additional = item.get("additional") or {}
    return {
        "source": "holidaycheck.ch",
        "source_url": f"https://www.holidaycheck.ch/hr/{HC_SLUG}/{HC_HOTEL}",
        "id": item.get("id"),
        "author": (user.get("firstName") or "").strip() or None,
        "title": item.get("title"),
        "rating": None,
        "recommendation": item.get("recommendation"),
        "traveled_with": item.get("traveledWith"),
        "published_at": ms_to_date(item.get("entryDate")),
        "visit_date": ms_to_date(item.get("travelDate")),
        "locale": item.get("originalLocale") or item.get("returnedLocale"),
        "cost_performance": additional.get("costPerformance"),
        "category_ratings": ratings,
        "confirmed_stay": bool(item.get("proofedReservation")),
        "text": "\n\n".join(parts).strip(),
    }


def collect_holidaycheck(max_pages: int = 250) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    empty_streak = 0
    for page in range(1, max_pages + 1):
        url = f"https://www.holidaycheck.ch/hr/{HC_SLUG}/{HC_HOTEL}?p={page}"
        try:
            html = fetch(url)
        except Exception as exc:  # noqa: BLE001
            print(f"[HC] page {page} fail: {exc}", flush=True)
            empty_streak += 1
            if empty_streak >= 3:
                break
            time.sleep(1)
            continue
        store = extract_js_object(html, '"HotelReviewStore":')
        if not store:
            print(f"[HC] page {page}: no store", flush=True)
            empty_streak += 1
            if empty_streak >= 3:
                break
            continue
        items = store.get("items") or []
        if not items:
            empty_streak += 1
            print(f"[HC] page {page}: empty (total={store.get('total')})", flush=True)
            if empty_streak >= 3:
                break
            continue
        empty_streak = 0
        added = 0
        for item in items:
            norm = normalize_hc_item(item)
            rid = norm.get("id")
            if rid and rid not in by_id and norm.get("text"):
                by_id[rid] = norm
                added += 1
        print(
            f"[HC] page {page}: +{added} items_on_page={len(items)} "
            f"total_unique={len(by_id)} store_total={store.get('total')}",
            flush=True,
        )
        # stop when page offset exceeds known total
        total = store.get("total") or 0
        offset = store.get("offset") or 0
        if total and offset + len(items) >= total:
            break
        time.sleep(0.2)
    return list(by_id.values())


def parse_tophotels_review(review_id: str, html: str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "lxml")
    text_el = soup.select_one(".js-review-text")
    text = text_el.get_text("\n", strip=True) if text_el else ""
    author_el = soup.select_one(".hreview__user-name")
    author = author_el.get_text(" ", strip=True) if author_el else None
    rate_el = soup.select_one("a.hreview__bb-rate b, .hreview__bb-rate b")
    rating = rate_el.get_text(strip=True) if rate_el else None
    cats: dict[str, str] = {}
    for div in soup.select(".hreview__bb-acomm, .hreview__bb-serv, .hreview__bb-food"):
        label = div.select_one("span")
        val = div.select_one("b")
        if label and val:
            cats[label.get_text(strip=True)] = val.get_text(strip=True)
    year_el = soup.select_one(".hreview__year-date")
    visit = re.sub(r"\s+", " ", year_el.get_text(" ", strip=True)) if year_el else None
    title = None
    for sel in ["h2", "h3", ".b-review__title", ".js-review-title"]:
        el = soup.select_one(sel)
        if el:
            t = el.get_text(" ", strip=True)
            if 5 < len(t) < 200 and "TopHotels" not in t and "Jaz" not in t[:3]:
                title = t
                break
    return {
        "source": "tophotels.ru",
        "source_url": f"https://tophotels.ru/review/{review_id}",
        "id": review_id,
        "author": author,
        "title": title,
        "rating": rating,
        "category_ratings": cats,
        "visit_period": visit,
        "recommended": bool(soup.select_one(".hreview__rec")),
        "confirmed_stay": bool(soup.select_one(".hreview__confirm")),
        "text": text,
    }


def collect_tophotels_ids() -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    for page in range(1, 41):
        url = f"https://tophotels.ru/hotel/al1811/reviews/list?page={page}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": UA, "X-Requested-With": "XMLHttpRequest"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        page_ids = list(dict.fromkeys(re.findall(r"/review/(\d+)", html)))
        unique = [i for i in page_ids if i not in seen]
        if not unique:
            break
        for i in unique:
            seen.add(i)
            ids.append(i)
        if len(unique) < 5:
            break
        time.sleep(0.15)
    return ids


def fetch_th(rid: str) -> dict[str, Any] | None:
    for attempt in range(4):
        try:
            html = fetch(f"https://tophotels.ru/review/{rid}")
            item = parse_tophotels_review(rid, html)
            if item.get("text"):
                return item
        except Exception:
            time.sleep(0.4 * (attempt + 1))
    return None


def refresh_tophotels() -> list[dict[str, Any]]:
    ids = collect_tophotels_ids()
    print(f"[TopHotels] ids={len(ids)}", flush=True)
    out: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futs = {pool.submit(fetch_th, rid): rid for rid in ids}
        done = 0
        for fut in concurrent.futures.as_completed(futs):
            done += 1
            item = fut.result()
            if item:
                out.append(item)
            if done % 50 == 0 or done == len(ids):
                print(f"[TopHotels] {done}/{len(ids)} ok={len(out)}", flush=True)
    out.sort(key=lambda r: int(r["id"]), reverse=True)
    return out


def load_existing_non_th() -> list[dict[str, Any]]:
    path = OUT_DIR / "reviews.all_sources.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return [r for r in data.get("reviews", []) if r.get("source") != "tophotels.ru"]


def format_review(idx: int, r: dict[str, Any]) -> str:
    lines = [f"### {idx}. {r.get('author') or 'Без имени'}"]
    meta = []
    if r.get("source"):
        meta.append(f"источник: [{r['source']}]({r.get('source_url') or '#'})")
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
        lines.append("- " + " · ".join(meta))
    cats = r.get("category_ratings") or {}
    if cats:
        cat_s = ", ".join(f"{k}: {v}" for k, v in cats.items() if v is not None)
        if cat_s:
            lines.append(f"- категории: {cat_s}")
    if r.get("title"):
        lines.append(f"\n**{str(r['title']).strip()}**\n")
    text = str(r.get("text") or "").strip()
    if text:
        lines.append(text)
    lines += ["", "---", ""]
    return "\n".join(lines)


def build_markdown(all_reviews: list[dict[str, Any]], by_source: dict[str, int]) -> str:
    now = datetime.now(timezone.utc).isoformat()
    lines = [
        f"# Отзывы об отеле {HOTEL_NAME}",
        "",
        "Максимально доступная выгрузка из открытых источников.",
        "",
        f"- Дата сбора: `{now}`",
        f"- Всего отзывов в файле: **{len(all_reviews)}**",
        "",
        "## Источники",
        "",
    ]
    for src, cnt in sorted(by_source.items(), key=lambda x: -x[1]):
        lines.append(f"- {src}: {cnt}")
    lines += [
        "",
        "## Покрытие и ограничения",
        "",
        "- **HolidayCheck** — пагинация HTML (`?p=`), полные тексты вкладок отзывов.",
        "- **TopHotels** — полный список `/reviews/list` + страницы `/review/{id}`.",
        "- **Onlinetours / OneTwoTrip** — встроенные JSON на страницах отелей.",
        "- **Booking.com / TripAdvisor / Google** — антибот/captcha в этой среде;",
        "  по публичным счётчикам: Booking ≈ 2 000+, TripAdvisor ≈ 1 600–1 800,",
        "  HolidayCheck indexed ≈ 2 100+.",
        "",
        "---",
        "",
        "## Все отзывы",
        "",
    ]
    for i, r in enumerate(all_reviews, 1):
        lines.append(format_review(i, r))
    return "\n".join(lines)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    hc = collect_holidaycheck()
    th = refresh_tophotels()
    other = [
        r
        for r in load_existing_non_th()
        if r.get("source") in {"onlinetours.ru", "onetwotrip.com"}
    ]

    all_reviews = hc + th + other
    by_source: dict[str, int] = {}
    for r in all_reviews:
        by_source[r["source"]] = by_source.get(r["source"], 0) + 1

    payload = {
        "hotel": HOTEL_NAME,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "total": len(all_reviews),
        "by_source": by_source,
        "reviews": all_reviews,
    }
    (OUT_DIR / "reviews.all_sources.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    md_path = OUT_DIR / "REVIEWS_ALL.md"
    md_path.write_text(build_markdown(all_reviews, by_source), encoding="utf-8")
    print(
        json.dumps(
            {
                "total": len(all_reviews),
                "by_source": by_source,
                "md_bytes": md_path.stat().st_size,
                "md_path": str(md_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
