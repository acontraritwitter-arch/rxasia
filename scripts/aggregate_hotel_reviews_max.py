#!/usr/bin/env python3
"""Collect maximum available reviews for Jaz Elite Casa Del Mar Beach.

Sources:
  - TopHotels (paginated list + full review pages)
  - Onlinetours (__INITIAL_STATE__)
  - OneTwoTrip (embedded JSON)
"""

from __future__ import annotations

import concurrent.futures
import html as html_lib
import json
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
OUT_DIR = Path("data/onlinetours/jaz-casa-del-mar-beach")
HOTEL_NAME = "Jaz Elite Casa Del Mar Beach"


def fetch(url: str, timeout: int = 60, headers: dict[str, str] | None = None) -> str:
    hdrs = {"User-Agent": UA, "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def strip_html(text: str) -> str:
    if not text:
        return ""
    text = html_lib.unescape(text.replace("&nbsp;", " ").replace("\xa0", " "))
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_date(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(value[:19], fmt).date().isoformat()
            except ValueError:
                continue
    return value


# ---------- TopHotels ----------

def collect_tophotels_ids(max_pages: int = 40) -> list[str]:
    ids: list[str] = []
    seen: set[str] = set()
    for page in range(1, max_pages + 1):
        url = f"https://tophotels.ru/hotel/al1811/reviews/list?page={page}"
        html = fetch(url, headers={"X-Requested-With": "XMLHttpRequest"})
        page_ids = re.findall(r'/review/(\d+)', html)
        unique = [i for i in dict.fromkeys(page_ids) if i not in seen]
        if not unique:
            break
        for i in unique:
            seen.add(i)
            ids.append(i)
        print(f"[TopHotels] page {page}: +{len(unique)} (total {len(ids)})", flush=True)
        if len(unique) < 5:
            break
        time.sleep(0.25)
    return ids


def parse_tophotels_review(review_id: str, html: str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "lxml")
    text_el = soup.select_one(".js-review-text")
    text = text_el.get_text("\n", strip=True) if text_el else ""

    title = None
    h = soup.select_one("h1, .review-title, .hreview__title")
    # On TH, title often after recommend block
    title_el = soup.select_one(".js-review-title, .review__title, .b-review-title")
    if title_el:
        title = title_el.get_text(" ", strip=True)

    # Rating big number
    rating = None
    rate_el = soup.select_one(".hreview__bb-rate b, .review-rate b, b.green")
    if rate_el:
        rating = rate_el.get_text(strip=True)

    # Category ratings
    cats: dict[str, str] = {}
    for div in soup.select(".hreview__bb-acomm, .hreview__bb-serv, .hreview__bb-food"):
        label = div.select_one("span")
        val = div.select_one("b")
        if label and val:
            cats[label.get_text(strip=True)] = val.get_text(strip=True)

    author = None
    author_el = soup.select_one(".hreview__user-name, .user-name, .review-author")
    if author_el:
        author = author_el.get_text(" ", strip=True)

    visit = None
    year_el = soup.select_one(".hreview__year-date")
    if year_el:
        visit = re.sub(r"\s+", " ", year_el.get_text(" ", strip=True))

    # pros/cons if present
    pros = cons = None
    for block in soup.select(".hreview__char, .review-plus, .review-minus"):
        label = block.get_text(" ", strip=True)
        if label.lower().startswith("плюс") or "Плюс" in label[:20]:
            pros = label
        if label.lower().startswith("минус") or "Минус" in label[:20]:
            cons = label

    # Better title from page structure: often a strong/bold heading near text
    if not title:
        for sel in ["h2", "h3", ".b-review__title"]:
            el = soup.select_one(sel)
            if el:
                t = el.get_text(" ", strip=True)
                if 5 < len(t) < 200 and "TopHotels" not in t:
                    title = t
                    break

    # Meta description sometimes holds short summary
    md = soup.select_one('meta[name="description"]')
    meta = md.get("content") if md else None

    recommended = bool(soup.select_one(".hreview__rec, .fa-thumbs-up"))
    confirmed = bool(soup.select_one(".hreview__confirm"))

    return {
        "source": "tophotels.ru",
        "source_url": f"https://tophotels.ru/review/{review_id}",
        "id": review_id,
        "author": author,
        "title": title,
        "rating": rating,
        "category_ratings": cats,
        "visit_period": visit,
        "recommended": recommended,
        "confirmed_stay": confirmed,
        "pros": pros,
        "cons": cons,
        "text": text,
        "meta": meta,
    }


def fetch_one_th(review_id: str) -> dict[str, Any] | None:
    url = f"https://tophotels.ru/review/{review_id}"
    for attempt in range(3):
        try:
            html = fetch(url)
            return parse_tophotels_review(review_id, html)
        except Exception as exc:  # noqa: BLE001
            time.sleep(0.5 * (attempt + 1))
            last = exc
    print(f"[TopHotels] fail {review_id}: {last}", flush=True)
    return None


def collect_tophotels() -> list[dict[str, Any]]:
    ids = collect_tophotels_ids()
    print(f"[TopHotels] fetching {len(ids)} full reviews...", flush=True)
    reviews: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(fetch_one_th, rid): rid for rid in ids}
        done = 0
        for fut in concurrent.futures.as_completed(futures):
            done += 1
            item = fut.result()
            if item and item.get("text"):
                reviews.append(item)
            if done % 25 == 0 or done == len(ids):
                print(f"[TopHotels] fetched {done}/{len(ids)}, ok={len(reviews)}", flush=True)
    reviews.sort(key=lambda r: int(r["id"]), reverse=True)
    return reviews


# ---------- Onlinetours ----------

def collect_onlinetours() -> list[dict[str, Any]]:
    url = "https://www.onlinetours.ru/oteli/egypt/hurgada/jaz-casa-del-mar-beach"
    html = fetch(url)
    m = re.search(
        r"var __INITIAL_STATE__ = (\{.*?\});\s*(?:</script>|var |window\.)",
        html,
        re.S,
    )
    if not m:
        print("[Onlinetours] no state", flush=True)
        return []
    state = json.loads(m.group(1))
    page = state["page"]
    group_map = {g["id"]: g["name"] for g in page.get("hotel_reviews_group_types", [])}
    out = []
    for r in page.get("hotel_reviews") or []:
        ratings = r.get("ratings") or {}
        out.append(
            {
                "source": "onlinetours.ru",
                "source_url": url,
                "author": r.get("author_name"),
                "published_at": parse_date(r.get("published_at")),
                "visit_date": parse_date(r.get("visit_date")),
                "group_type": group_map.get(r.get("group_type_id")),
                "rating": r.get("total_rating"),
                "category_ratings": {
                    "Питание": ratings.get("food"),
                    "Сервис": ratings.get("service"),
                    "Размещение": ratings.get("location"),
                },
                "text": strip_html(r.get("sanitized_text") or ""),
            }
        )
    print(f"[Onlinetours] {len(out)} reviews", flush=True)
    return out


# ---------- OneTwoTrip ----------

def collect_onetwotrip() -> list[dict[str, Any]]:
    url = "https://www.onetwotrip.com/ru/hotels/hotel/jaz-elite-casa-del-mar-beach-357361"
    html = fetch(url)
    out: list[dict[str, Any]] = []
    for m in re.finditer(r'"reviews"\s*:\s*(\[)', html):
        start = m.start(1)
        depth = 0
        end = None
        for i, ch in enumerate(html[start:], start):
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end is None:
            continue
        try:
            data = json.loads(html[start:end])
        except json.JSONDecodeError:
            continue
        if not data or not isinstance(data[0], dict):
            continue
        if "author" not in data[0] and "text" not in data[0]:
            continue
        for r in data:
            text_parts = []
            if r.get("pros"):
                text_parts.append(f"Плюсы: {r['pros']}")
            if r.get("cons"):
                text_parts.append(f"Минусы: {r['cons']}")
            if r.get("text"):
                text_parts.append(r["text"])
            out.append(
                {
                    "source": "onetwotrip.com",
                    "source_url": url,
                    "author": r.get("author"),
                    "visit_date": parse_date(r.get("housingDate")),
                    "rating": r.get("score"),
                    "rating_word": r.get("scoreWord"),
                    "room_type": r.get("roomType"),
                    "text": "\n\n".join(text_parts).strip(),
                }
            )
        break
    print(f"[OneTwoTrip] {len(out)} reviews", flush=True)
    return out


# ---------- Markdown ----------

def md_escape(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def format_review(idx: int, r: dict[str, Any]) -> str:
    lines = [f"### {idx}. {r.get('author') or 'Без имени'}"]
    meta = []
    if r.get("source"):
        meta.append(f"источник: [{r['source']}]({r.get('source_url') or '#'})")
    if r.get("rating") is not None:
        meta.append(f"оценка: **{r['rating']}**")
    if r.get("rating_word"):
        meta.append(str(r["rating_word"]))
    if r.get("published_at"):
        meta.append(f"опубликован: {r['published_at']}")
    if r.get("visit_date"):
        meta.append(f"визит: {r['visit_date']}")
    if r.get("visit_period"):
        meta.append(f"период: {r['visit_period']}")
    if r.get("group_type"):
        meta.append(f"компания: {r['group_type']}")
    if r.get("room_type"):
        meta.append(f"номер: {r['room_type']}")
    if r.get("confirmed_stay"):
        meta.append("проживание подтверждено")
    if r.get("recommended"):
        meta.append("рекомендует")
    if meta:
        lines.append("- " + " · ".join(meta))

    cats = r.get("category_ratings") or {}
    if cats:
        cat_s = ", ".join(f"{k}: {v}" for k, v in cats.items() if v is not None)
        if cat_s:
            lines.append(f"- категории: {cat_s}")

    if r.get("title"):
        lines.append(f"\n**{md_escape(str(r['title']))}**\n")

    text = md_escape(str(r.get("text") or ""))
    if text:
        lines.append(text)
    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def build_markdown(all_reviews: list[dict[str, Any]], by_source: dict[str, int]) -> str:
    now = datetime.now(timezone.utc).isoformat()
    lines = [
        f"# Отзывы об отеле {HOTEL_NAME}",
        "",
        "Собрано из открытых источников в интернете. Цель — максимальное покрытие.",
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
        "## Заметки о покрытии",
        "",
        "- **TopHotels** — основной массив полных текстов (пагинация `/reviews/list`).",
        "- **Onlinetours** — полный набор со страницы отеля (`__INITIAL_STATE__`).",
        "- **OneTwoTrip** — отзывы, встроенные в HTML страницы отеля.",
        "- **Booking.com / TripAdvisor / Google** в этой среде закрыты антиботом (пустой ответ / captcha),",
        "  поэтому их тысячи отзывов сюда не попали автоматически.",
        "  По публичным счётчикам: Booking ≈ 2 000+, TripAdvisor ≈ 1 600–1 800.",
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

    th = collect_tophotels()
    olt = collect_onlinetours()
    ott = collect_onetwotrip()

    all_reviews = th + olt + ott
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
    md = build_markdown(all_reviews, by_source)
    md_path = OUT_DIR / "REVIEWS_ALL.md"
    md_path.write_text(md, encoding="utf-8")
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
