#!/usr/bin/env python3
"""Parse hotel reviews embedded in an Onlinetours hotel page.

Onlinetours embeds the full review list for a hotel page inside
`window`/`var __INITIAL_STATE__` as `page.hotel_reviews`. For hotels
with a small review count this is the complete dataset (no extra API).

Usage:
  python3 scripts/onlinetours_hotel_reviews.py \\
    --url https://www.onlinetours.ru/oteli/egypt/hurgada/jaz-casa-del-mar-beach

  # or from a saved HTML file:
  python3 scripts/onlinetours_hotel_reviews.py --html /path/to/page.html
"""

from __future__ import annotations

import argparse
import csv
import html as html_lib
import json
import re
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median
from typing import Any
from urllib.parse import urlparse


USER_AGENT = (
    "Mozilla/5.0 (compatible; OnlinetoursReviewAggregator/1.0; +research)"
)


def fetch_html(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract_initial_state(html: str) -> dict[str, Any]:
    match = re.search(
        r"var __INITIAL_STATE__ = (\{.*?\});\s*(?:</script>|var |window\.)",
        html,
        re.S,
    )
    if not match:
        raise ValueError("Не найден __INITIAL_STATE__ в HTML страницы отеля")
    return json.loads(match.group(1))


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


def slug_from_url(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    return path.split("/")[-1] or "hotel"


def normalize_reviews(
    reviews: list[dict[str, Any]],
    group_types: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    group_map = {g["id"]: g["name"] for g in group_types}
    cleaned: list[dict[str, Any]] = []
    for review in reviews:
        ratings = review.get("ratings") or {}
        photos = []
        for photo in review.get("photos") or []:
            if isinstance(photo, dict):
                photos.append(
                    {
                        "thumb": photo.get("thumb"),
                        "large": photo.get("large")
                        or photo.get("url")
                        or photo.get("original")
                        or photo.get("preview"),
                    }
                )
        text = strip_html(review.get("sanitized_text") or "")
        cleaned.append(
            {
                "author": review.get("author_name"),
                "published_at": parse_date(review.get("published_at")),
                "visit_date": parse_date(review.get("visit_date")),
                "group_type_id": review.get("group_type_id"),
                "group_type": group_map.get(review.get("group_type_id")),
                "total_rating": review.get("total_rating"),
                "ratings": {
                    "food": ratings.get("food"),
                    "service": ratings.get("service"),
                    "location": ratings.get("location"),
                },
                "text": text,
                "photos": photos,
                "photos_count": len(photos),
                "text_length": len(text),
            }
        )
    return cleaned


THEME_KEYWORDS = {
    "пляж_море": ["пляж", "море", "лагун", "шезлонг", "заход"],
    "питание": [
        "еда",
        "питан",
        "ресторан",
        "кухн",
        "шведск",
        "а ля",
        "а-ля",
        "завтрак",
        "ужин",
        "десерт",
    ],
    "персонал_сервис": ["персонал", "сервис", "официант", "ресепш", "сотрудник"],
    "номера": ["номер", "кровать", "уборк", "ремонт", "розет"],
    "бассейн": ["бассейн"],
    "анимация_дети": ["анимац", "детск", "дискотек", "мини-клуб", "мини клуб"],
    "алкоголь": ["алкогол", "пиво", "вино", "коктейл", "бар"],
    "wifi": ["wifi", "wi-fi", "интернет"],
    "расположение": ["аэропорт", "располож", "трансфер"],
}


def rating_bucket(value: float) -> str:
    if value >= 9.5:
        return "9.5–10"
    if value >= 9.0:
        return "9.0–9.4"
    if value >= 8.0:
        return "8.0–8.9"
    if value >= 7.0:
        return "7.0–7.9"
    return "<7"


def aggregate(reviews: list[dict[str, Any]], hotel: dict[str, Any]) -> dict[str, Any]:
    totals = [r["total_rating"] for r in reviews if r["total_rating"] is not None]
    food = [r["ratings"]["food"] for r in reviews if r["ratings"]["food"] is not None]
    service = [
        r["ratings"]["service"] for r in reviews if r["ratings"]["service"] is not None
    ]
    location = [
        r["ratings"]["location"] for r in reviews if r["ratings"]["location"] is not None
    ]

    by_year: Counter[str] = Counter()
    for review in reviews:
        date_value = review["visit_date"] or review["published_at"]
        if date_value:
            by_year[str(date_value)[:4]] += 1

    theme_counts = {key: 0 for key in THEME_KEYWORDS}
    for review in reviews:
        text = review["text"].lower()
        for theme, keywords in THEME_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                theme_counts[theme] += 1

    total = len(reviews) or 1
    return {
        "reviews_total": len(reviews),
        "avg_total_rating": round(mean(totals), 2) if totals else None,
        "median_total_rating": median(totals) if totals else None,
        "min_total_rating": min(totals) if totals else None,
        "max_total_rating": max(totals) if totals else None,
        "avg_ratings": {
            "food": round(mean(food), 2) if food else None,
            "service": round(mean(service), 2) if service else None,
            "location": round(mean(location), 2) if location else None,
        },
        "official_category_ratings": hotel.get("total_rating_reviews"),
        "official_rating": hotel.get("rating"),
        "by_visit_year": dict(sorted(by_year.items())),
        "by_group_type": dict(Counter(r["group_type"] or "Не указано" for r in reviews)),
        "rating_distribution": dict(Counter(rating_bucket(v) for v in totals)),
        "photos_total": sum(r["photos_count"] for r in reviews),
        "avg_text_length": round(mean(r["text_length"] for r in reviews), 1)
        if reviews
        else 0,
        "theme_mentions_count": theme_counts,
        "theme_coverage_share": {
            key: round(value / total, 2) for key, value in theme_counts.items()
        },
    }


def hotel_card(hotel: dict[str, Any], fallback_url: str) -> dict[str, Any]:
    return {
        "id": hotel.get("id"),
        "display_name": hotel.get("display_name"),
        "old_name": hotel.get("old_name"),
        "stars": hotel.get("stars"),
        "rating": hotel.get("rating"),
        "reviews_count": hotel.get("reviews_count"),
        "category_ratings": hotel.get("total_rating_reviews"),
        "address": hotel.get("address"),
        "latitude": hotel.get("latitude"),
        "longitude": hotel.get("longitude"),
        "opening_year": hotel.get("opening_year"),
        "renovation_year": hotel.get("renovation_year"),
        "room_count": hotel.get("room_count"),
        "floor_count": hotel.get("floor_count"),
        "check_in_time": hotel.get("check_in_time"),
        "check_out_time": hotel.get("check_out_time"),
        "beach_description": hotel.get("beach_description"),
        "description": strip_html(hotel.get("description") or ""),
        "manager_description": strip_html(hotel.get("manager_description") or ""),
        "url": hotel.get("url") or fallback_url,
    }


def write_outputs(
    out_dir: Path,
    payload: dict[str, Any],
    raw_reviews: list[dict[str, Any]],
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "reviews.aggregated.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "reviews.raw.json").write_text(
        json.dumps(raw_reviews, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    with (out_dir / "reviews.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "author",
                "published_at",
                "visit_date",
                "group_type",
                "total_rating",
                "food",
                "service",
                "location",
                "photos_count",
                "text_length",
                "text",
            ],
        )
        writer.writeheader()
        for review in payload["reviews"]:
            writer.writerow(
                {
                    "author": review["author"],
                    "published_at": review["published_at"],
                    "visit_date": review["visit_date"],
                    "group_type": review["group_type"],
                    "total_rating": review["total_rating"],
                    "food": review["ratings"]["food"],
                    "service": review["ratings"]["service"],
                    "location": review["ratings"]["location"],
                    "photos_count": review["photos_count"],
                    "text_length": review["text_length"],
                    "text": review["text"],
                }
            )

    hotel = payload["hotel"]
    agg = payload["aggregation"]
    summary = f"""# {hotel.get("display_name") or "Hotel"} — отзывы Onlinetours

Источник: [{payload["url"]}]({payload["url"]})

Собрано: `{payload["scraped_at"]}`

## Отель
- ID: `{hotel.get("id")}`
- Название: {hotel.get("display_name")}
- Старое название: {hotel.get("old_name")}
- Звёзды: {hotel.get("stars")}
- Официальный рейтинг: **{hotel.get("rating")}**
- Отзывов: **{hotel.get("reviews_count")}**
- Оценки по категориям: {hotel.get("category_ratings")}

## Агрегация
- Средний total: **{agg.get("avg_total_rating")}** (медиана {agg.get("median_total_rating")}, min {agg.get("min_total_rating")}, max {agg.get("max_total_rating")})
- Средние категории: {agg.get("avg_ratings")}
- По годам визита: {agg.get("by_visit_year")}
- По типу компании: {agg.get("by_group_type")}
- Распределение оценок: {agg.get("rating_distribution")}
- Упоминания тем: {agg.get("theme_mentions_count")}

## Файлы
- `reviews.aggregated.json`
- `reviews.raw.json`
- `reviews.csv`
"""
    (out_dir / "SUMMARY.md").write_text(summary, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", help="URL страницы отеля на onlinetours.ru")
    parser.add_argument("--html", type=Path, help="Локальный HTML-файл страницы отеля")
    parser.add_argument(
        "--out",
        type=Path,
        help="Директория вывода (по умолчанию data/onlinetours/<slug>/)",
    )
    args = parser.parse_args()

    if not args.url and not args.html:
        parser.error("Нужен --url или --html")

    if args.html:
        html = args.html.read_text(encoding="utf-8", errors="replace")
        source_url = args.url or str(args.html)
    else:
        source_url = args.url
        html = fetch_html(source_url)

    state = extract_initial_state(html)
    page = state["page"]
    hotel = page["hotel"]
    raw_reviews = page.get("hotel_reviews") or []
    group_types = page.get("hotel_reviews_group_types") or []
    reviews = normalize_reviews(raw_reviews, group_types)

    payload = {
        "source": "onlinetours.ru",
        "method": "parse __INITIAL_STATE__.page.hotel_reviews from hotel page HTML",
        "url": source_url,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "hotel": hotel_card(hotel, source_url),
        "group_types": group_types,
        "reviews": reviews,
        "aggregation": aggregate(reviews, hotel),
    }

    out_dir = args.out or Path("data/onlinetours") / slug_from_url(source_url)
    write_outputs(out_dir, payload, raw_reviews)
    print(
        json.dumps(
            {
                "out_dir": str(out_dir),
                "hotel_id": payload["hotel"]["id"],
                "reviews_total": payload["aggregation"]["reviews_total"],
                "avg_total_rating": payload["aggregation"]["avg_total_rating"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
