# Problem statement (report-ready)

## Domain
Transportation: intercity bus travel and online ticketing (India).

## Business problem
Intercity bus operators in India price seats dynamically. redBus alone runs an algorithmic pricing engine (revMax) that changes fares about 15,000 times a day across roughly 40,000 buses [1]. The fare for the same route, operator, bus type and departure time therefore depends on when the ticket is bought. Travellers, corporate travel desks and institutional bulk bookers choose when to book by habit, either weeks ahead ("fares only go up") or at the last minute ("wait for a deal"). Neither habit is based on evidence for the route, operator and date in question, so buyers overpay on some trips and miss cheaper windows on others. Festival periods make the stakes higher, because private omnibus fares are not regulated and can jump far above normal levels [3], [4].

## Analytics objective
Collect listing-level fare data by web scraping public redBus search pages across several corridors and a 1 to 60 day booking window. Measure how days to departure, operator, bus class, occupancy, weekday and festival periods affect fares. Build (1) a regression model that predicts a listing's expected fare and (2) a classification model that labels a quoted fare **Book Now** (at least 5% cheaper than the same bus close to departure) or **Wait**. Turn the results into booking-timing rules for travellers, travel desks, platforms and operators.

## Why it matters
1. **Scale.** Intercity bus travel on redBus reached 147 million journeys in October 2025 to March 2026, up 24% year on year, with ₹142 billion in ticket value [2].
2. **Pricing is algorithmic, buyers are not.** Operators and platforms price with machine learning [1]; buyers still rely on rules of thumb.
3. **Festival surges hurt buyers and draw regulators.** In Deepavali 2025, Chennai-Madurai omnibus fares reached ₹4,500 against an approved ₹1,930-3,070, and the Tamil Nadu transport minister ordered operators back to approved limits [3].

## Cost & damage (measured mechanism + illustrative ₹ model)
- **Measured:** for private operators on ordinary dates, the same bus is **14.3% cheaper** 1-4 days before departure than 5-60 days before (median same-service fare index 85.7 vs 100). Festival departures are **20% above normal** (median).
- **Illustrative travel desk** (200 trips a month; trip mix, private share and average fare taken from the scraped sample): booking every ordinary-date private trip 5+ days ahead costs about **₹27,150 a month (~₹3.3 lakh a year)** more than booking them 1-4 days out.

## Success criteria (from the course brief)
- Problem statement approved at proposal stage, with importance and 2-3 objectives
- Own dataset collected by web scraping from public pages (not Kaggle/UCI/GitHub dumps), source and procedure documented
- Preprocessing, EDA, analytics methods from the syllabus, evaluation
- At least 3 recent published studies compared
- Results, business insights and recommendations; references cited

## What this is not
- Not an airline-fare Kaggle dataset
- Not a claim about redBus's or any operator's internal pricing rules; only publicly displayed fares were observed
- Not a longitudinal study of single tickets: the data is one scrape day across 13 departure dates

## Sources
1. Autocar Professional, "The algorithm that adjusts bus prices 15,000 times a day," 3 Oct 2025. https://www.autocarpro.in/news/the-algorithm-that-adjusts-bus-prices-15000-times-a-day-129061
2. Autocar Professional, "Intercity bus passenger volumes rise 24% in second half of FY2026: redBus report," 21 May 2026. https://www.autocarpro.in/news/intercity-bus-passenger-volumes-rise-24-percent-in-second-half-of-fy2026-redbus-report-132718
3. Free Press Journal, "Tamil Nadu's omnibus operators raise fares for festive season despite state transport department's warnings," 13 Oct 2025. https://www.freepressjournal.in/business/tamil-nadus-omnibus-operators-raise-fares-despite-state-transport-departments-warnings
4. The News Minute, "How TN omnibus operators overcharge during festive season and get away with it," 15 Oct 2019. https://www.thenewsminute.com/tamil-nadu/how-tn-omnibus-operators-overcharge-during-festive-season-and-get-away-it-110559
