# Data collection procedure

## Source
[redBus](https://www.redbus.in), India's largest online bus-ticketing platform. Route search pages such as `https://www.redbus.in/bus-tickets/bangalore-to-chennai` list every bus on sale for a date and are public (no login).

## Method: web scraping
1. **Endpoint.** The search page loads its listings from a JSON endpoint called by the site's own front end:
   `POST /rpw/api/searchResults?fromCity=<id>&toCity=<id>&DOJ=<dd-Mon-yyyy>&limit=100&offset=<k>&groupId=<g>...`
   City IDs were read from each route page (Bengaluru 122, Chennai 123, Hyderabad 124, Madurai 126, Pune 130, Vijayawada 134, Coimbatore 141, Mumbai 462, Delhi 733, Jaipur 807).
2. **Coverage.** 8 corridors × 13 departure dates (1, 2, 3, 4, 5, 6, 7, 10, 14, 21, 30, 45 and 60 days after the scrape date, 25 Sep 2026) = 104 searches.
3. **Paging.** Results were read 100 at a time until a page returned fewer than 100 rows, so every listed bus was captured, not only the first screen (Mumbai-Pune was capped at 600 per date; about 620 exist).
4. **Government groups.** State corporations (APSRTC, TGSRTC, KSRTC, RSRTC, ...) are shown as collapsed groups; a second pass expanded each group with `groupId=<operatorId>`.
5. **Why in a browser.** Script requests (curl, Python) could not reach the site from the analysis environment, so the collector ran as a script inside a normal browser session on redbus.in. The exact script is [`scraper/redbus_collector.js`](../scraper/redbus_collector.js); a Python equivalent is in `analysis.ipynb`.
6. **Politeness.** 1.2-1.5 s pause between requests; a few hundred requests in total over roughly 20 minutes; each page fetched once.

## Fields kept (raw file)
`scrape_date, source, destination, departure_date, operator, bus_type, is_ac, is_sleeper, departure_time, arrival_time, duration_min, rating, num_reviews, seats_available, total_seats, fare_min, fare_max, via, service_id`

`fare_min` (cheapest seat shown) is the fare analysed. `seats_available` / `total_seats` refer to the redBus seat map only; operators also sell through other channels.

## Output
| File | Rows | Notes |
|---|---:|---|
| `data/raw/bus_fares_raw_2026-09-25.csv` | 32,372 | as collected |
| `data/cleaned/bus_fares_clean.csv` | 31,838 | cleaned, derived features added, service code replaced by an integer key |

## Ethics and privacy
Only publicly displayed listing information was collected: no login, no booking, no passenger or personal data. The operator service code identifies a bus schedule, not a person, and is anonymised in the cleaned file. Data is used for academic purposes only.
