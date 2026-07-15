# Jaz Elite Casa Del Mar Beach — свод отзывов

Главный файл: [`REVIEWS_ALL.md`](./REVIEWS_ALL.md) (**2834** отзывов).

## Источники в файле
- holidaycheck.ch: 2135
- tophotels.ru: 642
- onetwotrip.com: 36
- onlinetours.ru: 11
- tripadvisor.co.uk: 10

## Booking / TripAdvisor
HTTP из датацентра режется антиботом (JS-challenge / captcha).  
Инструкция по Playwright-обходу: [`PLAYWRIGHT.md`](./PLAYWRIGHT.md)  
Скрипт: `scripts/scrape_booking_tripadvisor_playwright.py`

## Сопутствующие файлы
- `reviews.all_sources.json` — полный корпус
- `reviews.aggregated.json` / `reviews.csv` — ранняя выгрузка Onlinetours
