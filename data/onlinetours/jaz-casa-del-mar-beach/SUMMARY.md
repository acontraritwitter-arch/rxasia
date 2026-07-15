# Jaz Elite Casa Del Mar Beach — свод отзывов

Главный файл: [`REVIEWS_ALL.md`](./REVIEWS_ALL.md) (**4147** отзывов).

## Источники в файле
- holidaycheck.ch: 2135
- booking.com: 1313
- tophotels.ru: 642
- onetwotrip.com: 36
- onlinetours.ru: 11
- tripadvisor.co.uk: 10

## Booking / TripAdvisor
- **Booking.com**: Playwright + GraphQL `ReviewList` — выгружено **1313** текстовых отзывов из ~2121 на сайте (часть без текста/оценко-only отброшена).
- **TripAdvisor**: в этой среде по-прежнему captcha; скрипт готов для локального запуска с `--headed` / residential proxy.

Инструкция: [`PLAYWRIGHT.md`](./PLAYWRIGHT.md)

## Сопутствующие файлы
- `reviews.all_sources.json` — полный корпус
- `playwright_run_booking.json` — сырой прогон Booking
