# BookSmart: Predicting Optimal Booking Timing for Intercity Bus Travel Using Web-Scraped Fare Data

**Business Analytics - Individual Case Study**
Deepak Senthilkumar · CB.SC.U4CSE23267 · CSE-C

## Problem statement

Intercity bus operators in India price seats dynamically, so the same bus costs different amounts depending on when the ticket is bought. Travellers and corporate travel desks decide when to book on instinct, which leads to overpaying on some trips and missing cheaper windows on others. This study uses scraped fare listings to measure how the booking window, operator, bus class, occupancy and festival periods affect fares, and builds models that predict fares and tell a buyer whether to **book now** or **wait**.

## Objectives

1. Identify the factors that drive quoted intercity bus fares.
2. Predict the expected fare of a listing (regression).
3. Classify a quoted fare as **Book Now** or **Wait** (classification).
4. Compare booking-window behaviour across operators and corridors.

## Data collection

| | |
|---|---|
| Source | [redBus](https://www.redbus.in) public search-results pages (no login) |
| Method | Web scraping of the JSON endpoint that the search page itself calls, run in a browser session because the site refuses plain script requests; 1.2–1.5 s pause between requests; government-operator groups expanded in a second pass |
| Scrape date | 25 September 2026 |
| Coverage | 8 corridors (Bengaluru–Chennai, Bengaluru–Hyderabad, Bengaluru–Coimbatore, Chennai–Coimbatore, Chennai–Madurai, Hyderabad–Vijayawada, Mumbai–Pune, Delhi–Jaipur) × 13 departure dates (1, 2, 3, 4, 5, 6, 7, 10, 14, 21, 30, 45, 60 days ahead) |
| Records | 32,372 raw listings, 19 attributes, 981 operators → 31,838 after cleaning |
| Personal data | None. Only public listing information was collected; operator service codes are replaced by integer keys in the cleaned file |

The collector code is included in `analysis.ipynb` (section 3).

## Repository layout

```
README.md
analysis.ipynb                 # preprocessing, EDA, models, evaluation, outputs
Case_Study_Report.pdf          # final report (Section A format)
Case_Study_Report.docx         # editable source of the report
data/
  raw/bus_fares_raw_2026-09-25.csv   # scraped data as collected
  cleaned/bus_fares_clean.csv        # cleaned, anonymised dataset used for analysis
figures/                       # charts saved by the notebook
```

Run `analysis.ipynb` from the repository root (Python 3, pandas, numpy, matplotlib, seaborn, scikit-learn).

## Analytics methods

- **Same-service fare index:** each fare divided by the median fare of the same bus service across all dates, which isolates timing from bus mix. Checked with same-weekday date pairs.
- **Regression (target = log fare):** Multiple Linear Regression (baseline), Random Forest, Gradient Boosting; 80/20 split + 5-fold CV.
- **Classification (Book Now / Wait):** label = the listing is at least 5% cheaper than the same service's fare 1–3 days before departure (non-festival dates); Logistic Regression and Random Forest vs a majority-class baseline.

## Key results

- **Late booking is usually cheaper.** For private operators on ordinary dates, the same bus is **14.3% cheaper** in the last 1–4 days (median fare index 85.7 vs 100). Buses are only about 31% sold the day before departure, so operators cut fares to fill seats. 36 of 56 operators cut fares by more than 5%; none raise them.
- **Festivals reverse the rule.** Festival departures (Gandhi Jayanti weekend, Dussehra, Diwali–Chhath) are **20% above normal** in the median, and 60–66% above normal on the Coimbatore corridors.
- **Government buses are flat.** APSRTC, TGSRTC and RSRTC fares do not change with the booking window.
- **Fare regression:** Random Forest reaches test R² 0.83 on log fare (MAE ₹282, MAPE 18.8%), against 0.58 for linear regression.
- **Book Now / Wait classifier:** Random Forest reaches ROC-AUC 0.89 and F1 (Book Now) 0.55, and catches 71% of real bargains.
- **Recommendation:** on ordinary dates, book private buses 1–4 days out; book festival and Friday departures early; book government buses whenever convenient.

## References

1. redBus, bus ticket search results, https://www.redbus.in (data collected 25 Sep 2026).
2. Gaggero, A. A., Ogrzewalla, L., & Bubalo, B. (2019). Pricing of the long-distance bus service in Europe: The case of Flixbus. *Economics of Transportation*, 19, 100120. https://doi.org/10.1016/j.ecotra.2019.100120
3. Branda, F., Marozzo, F., & Talia, D. (2020). Ticket sales prediction and dynamic pricing strategies in public transport. *Big Data and Cognitive Computing*, 4(4), 36. https://doi.org/10.3390/bdcc4040036
4. Stavinova, E., Chunaev, P., & Bochenina, K. (2021). Forecasting railway ticket dynamic price with Google Trends open data. *Procedia Computer Science*, 193, 333–342. https://doi.org/10.1016/j.procs.2021.10.034
5. Degife, W. A., & Lin, B.-S. (2023). Deep-learning-powered GRU model for flight ticket fare forecasting. *Applied Sciences*, 13(10), 6032. https://doi.org/10.3390/app13106032
6. Arnerić, J., & Obadić, L. (2026). Key factors in dynamic pricing of FlixBus fares: A panel analysis of international and domestic routes in Croatia. *Research in Transportation Economics*, 118, 101794. https://doi.org/10.1016/j.retrec.2026.101794
7. HappyFares (2026). India festive travel calendar 2026. https://www.happyfares.in/blog/diwali-festive-season-flight-guide-2026/
8. Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *JMLR*, 12, 2825–2830.
9. Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5–32.
