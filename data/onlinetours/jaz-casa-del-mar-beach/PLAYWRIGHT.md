# Playwright-скрейперы Booking + TripAdvisor

Скрипт: [`../scripts/scrape_booking_tripadvisor_playwright.py`](../scripts/scrape_booking_tripadvisor_playwright.py)

## Зачем

`curl`/обычный HTTP из датацентра часто блокируются. Playwright с Chromium обходит часть защиты.

**Статус прогонов в cloud-среде:**
- **Booking.com** — работает через UI reviews + GraphQL `ReviewList` (`hotelId=314504`). Снято **1313** текстовых отзывов.
- **TripAdvisor** — всё ещё captcha на datacenter IP; нужен `--headed` и/или residential proxy локально.

## Установка

```bash
pip install -r scripts/requirements-scraping.txt
playwright install chromium
```

## Запуск

### 1. Booking (первые N страниц reviewlist)

```bash
python3 scripts/scrape_booking_tripadvisor_playwright.py booking \
  --headed \
  --max-pages 40 \
  --save-storage ./data/onlinetours/jaz-casa-del-mar-beach/storage_booking.json
```

Если вылезла captcha — решите её в окне браузера и нажмите Enter в терминале.

### 2. TripAdvisor (`or5`, `or10`, …)

```bash
python3 scripts/scrape_booking_tripadvisor_playwright.py tripadvisor \
  --headed \
  --max-pages 100 \
  --storage-state ./data/onlinetours/jaz-casa-del-mar-beach/storage_booking.json \
  --save-storage ./data/onlinetours/jaz-casa-del-mar-beach/storage_ta.json
```

### 3. Оба источника + merge в `REVIEWS_ALL.md`

```bash
export RESIDENTIAL_PROXY='http://user:pass@host:port'
python3 scripts/scrape_booking_tripadvisor_playwright.py both \
  --headed \
  --proxy "$RESIDENTIAL_PROXY" \
  --max-pages 80 \
  --storage-state ./data/onlinetours/jaz-casa-del-mar-beach/storage_ta.json
```

Результат мержится в:

- `reviews.all_sources.json`
- `REVIEWS_ALL.md`

Сырой прогон: `playwright_run_booking.json` / `playwright_run_tripadvisor.json`.

## Рекомендации против бана

1. **Residential / mobile proxy** (datacenter почти сразу режется).
2. **`--headed`** на первом прогоне + сохранить `--storage-state`.
3. Малые `max-pages`, паузы уже встроены (1–3.5 c).
4. Один отель за раз, без параллельных вкладок.
5. Не использовать captcha-solving сервисы — только ручной проход challenge.

## Ожидаемый объём

| Источник | Публичный счётчик | Реалистично снять Playwright’ом |
|---|---|---|
| Booking | ~2 000+ | почти все при стабильной сессии |
| TripAdvisor | ~1 600–1 800 | высокая доля при хорошем IP |

Дедуп по `(source, author, title, text[:160])` относительно уже собранного корпуса (HolidayCheck / TopHotels / …).
