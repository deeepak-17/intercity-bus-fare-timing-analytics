"""Generate the README figures in assets/images/.

Run from the repository root:  python assets/generate_figures.py
Uses only data/cleaned/bus_fares_clean.csv (no network). Numbers shown in the
cost model are computed here from the dataset; illustrative inputs are labelled.
"""
from pathlib import Path
import textwrap

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "images"
OUT.mkdir(parents=True, exist_ok=True)
DATA = ROOT / "data" / "cleaned" / "bus_fares_clean.csv"

NAVY, NAVY2 = "#0F2744", "#1E3A5F"
TEAL, AMBER, BLUE = "#0D9488", "#D97706", "#1D4ED8"   # validated categorical set
INK, MUTED, GRID = "#1F2937", "#64748B", "#E2E8F0"
LIGHT, WHITE = "#F8FAFC", "#FFFFFF"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.edgecolor": GRID, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED})


def save(fig, name):
    fig.savefig(OUT / name, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print("wrote", OUT / name)


def card(ax, x, y, w, h, edge, face=LIGHT, lw=2.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor=face, edgecolor=edge, linewidth=lw))


def wrap(text, width):
    return "\n".join(textwrap.wrap(text, width))


# ------------------------------------------------------------------ data-derived numbers
df = pd.read_csv(DATA)
svc_med = df.groupby("service_key")["fare"].transform("median")
svc_n = df.groupby("service_key")["fare"].transform("size")
df["svc_index"] = 100 * df["fare"] / svc_med
panel = df[svc_n >= 5]
priv_ord = panel[(panel["is_govt"] == 0) & (panel["is_festival"] == 0)]
near = priv_ord[priv_ord["days_to_departure"] <= 4]["svc_index"].median()
far = priv_ord[priv_ord["days_to_departure"] >= 5]["svc_index"].median()
DISCOUNT = 1 - near / far                                           # measured
fest = panel[panel["is_govt"] == 0].groupby("is_festival")["svc_index"].median()
FEST_PREMIUM = fest[1] / fest[0] - 1                                # measured
P_PRIVATE = 1 - df["is_govt"].mean()                                # measured (sample mix)
P_ORDINARY = 1 - df["is_festival"].mean()                           # measured (sample mix)
early = df[(df["is_govt"] == 0) & (df["is_festival"] == 0) & (df["days_to_departure"] >= 5)]
EARLY_FARE = early["fare"].mean()                                   # measured
TRIPS = 200                                                         # illustrative input


# ------------------------------------------------------------------ 1. hero banner
def fig_hero():
    fig, ax = plt.subplots(figsize=(12.5, 4.0), facecolor=NAVY)
    ax.set_facecolor(NAVY); ax.set_xlim(0, 12.5); ax.set_ylim(0, 4); ax.axis("off")
    ax.text(0.45, 3.15, "BUSINESS ANALYTICS CASE STUDY", color="#5EEAD4", fontsize=11, fontweight="bold")
    ax.text(0.45, 2.05, "BookSmart: When Should You Book\nan Intercity Bus in India?", color=WHITE,
            fontsize=21, fontweight="bold", linespacing=1.3)
    ax.text(0.45, 0.55, "Web-scraped redBus fares  ·  EDA  ·  Regression  ·  Book Now / Wait classifier",
            color="#CBD5E1", fontsize=11)
    tiles = [(f"{len(df):,}", "clean listings"), (f"-{100*DISCOUNT:.0f}%", "late booking,\nordinary dates"),
             (f"+{100*FEST_PREMIUM:.0f}%", "festival\ndepartures")]
    for i, (big, small) in enumerate(tiles):
        x = 8.35 + i * 1.38
        card(ax, x, 0.75, 1.22, 2.5, TEAL if i != 2 else AMBER, face=NAVY2)
        ax.text(x + 0.61, 2.35, big, ha="center", va="center", color=WHITE, fontsize=15, fontweight="bold")
        ax.text(x + 0.61, 1.35, small, ha="center", va="center", color="#CBD5E1", fontsize=8)
    save(fig, "hero_banner.png")


# ------------------------------------------------------------------ 2. problem flow
def fig_problem_flow():
    fig, ax = plt.subplots(figsize=(12.5, 5.2), facecolor=WHITE)
    ax.set_xlim(0, 12.5); ax.set_ylim(0, 5.6); ax.axis("off")
    ax.set_title("How guesswork on booking timing turns into overpayment", fontsize=14,
                 fontweight="bold", color=NAVY, pad=10)
    steps = [("Operators price\ndynamically\n(revMax: 15,000\nchanges a day)", BLUE),
             ("Fares move with\nbooking window,\noperator, festival,\nweekday", BLUE),
             ("Buyers decide\nby instinct\n('book early' or\n'wait for a deal')", AMBER),
             ("Overpay on some\ntrips, miss cheaper\nwindows on others", AMBER)]
    xs = [0.3, 3.4, 6.5, 9.6]
    for (t, col), x in zip(steps, xs):
        card(ax, x, 2.75, 2.6, 2.3, col)
        ax.text(x + 1.3, 3.9, t, ha="center", va="center", fontsize=10, color=INK)
    for x in xs[:-1]:
        ax.annotate("", xy=(x + 3.05, 3.9), xytext=(x + 2.65, 3.9),
                    arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2))
    card(ax, 0.6, 0.35, 11.3, 1.75, TEAL, face="#ECFDF5")
    ax.text(6.25, 1.22, "BookSmart: scrape real fares  →  measure the timing effect on the same bus  →\n"
            "predict fares  →  flag Book Now / Wait  →  timing rules by operator, corridor and festival",
            ha="center", va="center", fontsize=10, color=INK, fontweight="bold")
    ax.annotate("", xy=(6.25, 2.15), xytext=(6.25, 2.7), arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2))
    save(fig, "problem_flow.png")


# ------------------------------------------------------------------ 3. damage layers
def fig_damage_layers():
    fig, ax = plt.subplots(figsize=(12.5, 3.2), facecolor=WHITE)
    ax.set_xlim(0, 12.5); ax.set_ylim(0, 3.2); ax.axis("off")
    ax.set_title("Three layers of damage from uninformed booking timing", fontsize=14, fontweight="bold",
                 color=NAVY, pad=8)
    layers = [
        ("TRAVELLER", AMBER, f"Booking a private bus early on an ordinary date costs about "
         f"{100*DISCOUNT:.0f}% more than the same bus 1-4 days out (measured, same-service median)."),
        ("CORPORATE TRAVEL DESK", AMBER, "Hundreds of trips a month booked by habit: the per-ticket gap "
         "compounds into lakhs a year (worked model below)."),
        ("PLATFORM & OPERATOR", BLUE, "Buyers who feel overcharged lose trust; festival surcharges draw "
         "regulator warnings (Tamil Nadu, Deepavali 2025)."),
    ]
    for i, (head, col, body) in enumerate(layers):
        x = 0.25 + i * 4.1
        card(ax, x, 0.15, 3.85, 2.6, col)
        ax.text(x + 0.25, 2.4, head, fontsize=10.5, fontweight="bold", color=col)
        ax.text(x + 0.25, 2.0, wrap(body, 36), fontsize=10, color=INK, va="top", linespacing=1.45)
    save(fig, "damage_layers.png")


# ------------------------------------------------------------------ 4. cost model chart
def cost_model():
    trips_ord_priv = TRIPS * P_PRIVATE * P_ORDINARY
    spend_early = trips_ord_priv * EARLY_FARE
    spend_timed = spend_early * (1 - DISCOUNT)
    return trips_ord_priv, spend_early, spend_timed


def fig_cost():
    n, early_spend, timed_spend = cost_model()
    fig, ax = plt.subplots(figsize=(10, 4.4), facecolor=WHITE)
    vals = [early_spend, timed_spend]
    labels = ["Habit: book every trip\n5+ days ahead", "Data-timed: book ordinary-date\nprivate trips 1-4 days out"]
    bars = ax.barh(labels, vals, color=[AMBER, TEAL], height=0.5)
    for b, v in zip(bars, vals):
        ax.text(v + 2500, b.get_y() + b.get_height() / 2, f"Rs {v:,.0f}", va="center", fontsize=11, color=INK,
                fontweight="bold")
    ax.invert_yaxis(); ax.set_xlim(0, max(vals) * 1.25)
    ax.set_xlabel(f"Monthly spend on {n:.0f} ordinary-date private trips (Rs)")
    ax.spines[["top", "right", "left"]].set_visible(False); ax.grid(axis="x", color=GRID); ax.set_axisbelow(True)
    gap = early_spend - timed_spend
    ax.set_title(f"Illustrative travel desk ({TRIPS} trips/month): habit costs about Rs {gap:,.0f} a month\n"
                 f"(~Rs {12*gap/1e5:.1f} lakh a year) on ordinary-date private-bus trips", fontsize=12,
                 fontweight="bold", color=NAVY, loc="left")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    save(fig, "cost_damage_estimate.png")


# ------------------------------------------------------------------ 5. news cards
NEWS = [
    ("INDUSTRY", "redBus changes bus fares 15,000 times a day",
     "Its revMax engine uses demand signals from 2-3 million daily searches across ~40,000 buses; operators "
     "previously priced on 'gut feel'.", "Autocar Professional · 3 Oct 2025"),
    ("MARKET", "147 million intercity bus journeys in six months",
     "redBus BusTrack Oct 2025-Mar 2026: +24% year on year, Rs 142 bn ticket value, 72% AC buses, "
     "77% average occupancy.", "Autocar Professional · 21 May 2026"),
    ("FESTIVAL PRICING", "Deepavali bus fares hit Rs 4,500 in Tamil Nadu",
     "Chennai-Madurai fares up to Rs 4,500 against an approved Rs 1,930-3,070; the transport minister "
     "ordered operators back to approved limits.", "Free Press Journal · 13 Oct 2025"),
    ("REGULATION", "Why festive overcharging goes unchecked",
     "Omnibuses are 'contract carriages', so the state cannot regulate their fares; Bengaluru-Chennai "
     "sleepers nearly doubled at weekends.", "The News Minute · 15 Oct 2019"),
]


def fig_news():
    fig, ax = plt.subplots(figsize=(12.5, 6.4), facecolor=WHITE)
    ax.set_xlim(0, 12.5); ax.set_ylim(0, 6.4); ax.axis("off")
    ax.set_title("News & industry evidence behind the problem", fontsize=14, fontweight="bold", color=NAVY)
    for i, (tag, head, body, src) in enumerate(NEWS):
        x = 0.2 + (i % 2) * 6.2; y = 3.3 - (i // 2) * 3.15
        card(ax, x, y, 5.9, 2.85, GRID, lw=1.5)
        ax.add_patch(FancyBboxPatch((x + 0.08, y + 2.35), 5.74, 0.4, boxstyle="round,pad=0,rounding_size=0.08",
                                    facecolor=NAVY, edgecolor="none"))
        ax.text(x + 2.95, y + 2.55, tag, ha="center", va="center", fontsize=9, fontweight="bold", color="#5EEAD4")
        ax.text(x + 0.25, y + 2.05, wrap(head, 52), fontsize=11, fontweight="bold", color=INK, va="top")
        ax.text(x + 0.25, y + 1.45, wrap(body, 60), fontsize=9.3, color=INK, va="top", linespacing=1.4)
        ax.text(x + 0.25, y + 0.22, src, fontsize=8.5, color=TEAL, style="italic")
    save(fig, "news_cards.png")


# ------------------------------------------------------------------ 6. research paper cards
PAPERS = [
    ("2019", "Gaggero, Ogrzewalla & Bubalo", "Economics of Transportation",
     "Scraped Flixbus fares 28 to 1 days out; fares rise with seats sold."),
    ("2020", "Branda, Marozzo & Talia", "Big Data & Cognitive Computing",
     "3.23M ticketing events; 95% purchase-prediction accuracy, +9% revenue."),
    ("2021", "Stavinova, Chunaev & Bochenina", "Procedia Computer Science",
     "Rail fares + Google Trends; MV-LSTM MAPE 3.67% vs 4.25%."),
    ("2023", "Degife & Lin", "Applied Sciences",
     "1.03M airline records; GRU beats LSTM, MLP and classic ML."),
    ("2026", "Arneric & Obadic", "Research in Transportation Economics",
     "24 FlixBus routes; occupancy does not drive posted fares."),
]


def fig_papers():
    fig, ax = plt.subplots(figsize=(12.5, 3.9), facecolor=WHITE)
    ax.set_xlim(0, 12.5); ax.set_ylim(0, 3.9); ax.axis("off")
    ax.set_title("Published studies compared in the report (Section 5)", fontsize=14, fontweight="bold", color=NAVY)
    for i, (yr, auth, venue, finding) in enumerate(PAPERS):
        x = 0.15 + i * 2.48
        card(ax, x, 0.15, 2.33, 3.35, BLUE if i % 2 == 0 else TEAL, lw=1.6)
        ax.text(x + 0.18, 3.1, yr, fontsize=14, fontweight="bold", color=NAVY, va="top")
        ax.text(x + 0.18, 2.55, wrap(auth, 20), fontsize=9, fontweight="bold", color=INK, va="top")
        ax.text(x + 0.18, 1.85, wrap(venue, 24), fontsize=8.3, color=MUTED, style="italic", va="top")
        ax.text(x + 0.18, 1.2, wrap(finding, 25), fontsize=8.5, color=INK, va="top", linespacing=1.35)
    save(fig, "research_papers.png")


# ------------------------------------------------------------------ 7. evidence map
def fig_evidence_map():
    fig, ax = plt.subplots(figsize=(12.5, 5.6), facecolor=WHITE)
    ax.set_xlim(0, 12.5); ax.set_ylim(0, 5.6); ax.axis("off")
    ax.set_title("Evidence map: sources → claims → problem statement", fontsize=14, fontweight="bold", color=NAVY)
    left = [("revMax: 15,000 fare changes/day", 4.55), ("BusTrack: 147M trips in 6 months", 3.55),
            ("TN Deepavali fares up to Rs 4,500", 2.55), ("Omnibus fares unregulated", 1.55),
            ("5 published pricing studies", 0.55)]
    mid = [("Fares are dynamic and\nalgorithmic", 4.05, [0]), ("Large, growing market", 2.9, [1]),
           ("Festival surges hurt buyers", 1.85, [2, 3]), ("Method gap: buyer-side timing", 0.7, [4])]
    for t, y in left:
        card(ax, 0.2, y - 0.35, 3.7, 0.7, BLUE, lw=1.4)
        ax.text(2.05, y, t, ha="center", va="center", fontsize=9.3, color=INK)
    for t, y, links in mid:
        card(ax, 5.0, y - 0.42, 3.0, 0.84, AMBER, lw=1.6)
        ax.text(6.5, y, t, ha="center", va="center", fontsize=9.3, color=INK, fontweight="bold")
        for li in links:
            ax.annotate("", xy=(5.0, y), xytext=(3.9, left[li][1]),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2))
        ax.annotate("", xy=(9.2, 2.6), xytext=(8.0, y), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2))
    card(ax, 9.2, 1.4, 3.1, 2.4, TEAL, face="#ECFDF5", lw=2.2)
    ax.text(10.75, 2.6, "PS: buyers need\nevidence on WHEN\nto book a bus", ha="center", va="center",
            fontsize=11, fontweight="bold", color=INK)
    save(fig, "evidence_map.png")


# ------------------------------------------------------------------ 8. differentiation
def fig_differentiation():
    rows = [("Kaggle / UCI fare dataset", "32,372 listings scraped from redBus for this study"),
            ("Airline fares", "Indian intercity buses, 8 corridors, 981 operators"),
            ("Average fare by date (mixes buses)", "Same-service index: the same bus across 13 dates"),
            ("Predict price only", "Price model + Book Now / Wait decision model"),
            ("Assumes 'book early' is right", "Shows late booking is cheaper on ordinary dates")]
    fig, ax = plt.subplots(figsize=(12.5, 4.4), facecolor=WHITE)
    ax.set_xlim(0, 12.5); ax.set_ylim(0, 4.4); ax.axis("off")
    ax.set_title("How this project differs from a typical fare-prediction project", fontsize=14,
                 fontweight="bold", color=NAVY)
    ax.text(3.1, 3.85, "Typical project", ha="center", fontsize=11, fontweight="bold", color=AMBER)
    ax.text(9.2, 3.85, "BookSmart", ha="center", fontsize=11, fontweight="bold", color=TEAL)
    for i, (a, b) in enumerate(rows):
        y = 3.25 - i * 0.72
        card(ax, 0.3, y - 0.28, 5.6, 0.56, AMBER, lw=1.2)
        card(ax, 6.4, y - 0.28, 5.6, 0.56, TEAL, face="#ECFDF5", lw=1.2)
        ax.text(3.1, y, a, ha="center", va="center", fontsize=9.5, color=INK)
        ax.text(9.2, y, b, ha="center", va="center", fontsize=9.5, color=INK)
        ax.annotate("", xy=(6.35, y), xytext=(5.95, y), arrowprops=dict(arrowstyle="-|>", color=MUTED))
    save(fig, "differentiation.png")


if __name__ == "__main__":
    n, e, t = cost_model()
    print(f"discount {DISCOUNT:.3f}  festival {FEST_PREMIUM:.3f}  private {P_PRIVATE:.3f}  ordinary {P_ORDINARY:.3f}"
          f"  early fare {EARLY_FARE:.0f}  trips {n:.1f}  early {e:,.0f}  timed {t:,.0f}  gap {e-t:,.0f}")
    fig_hero(); fig_problem_flow(); fig_damage_layers(); fig_cost(); fig_news(); fig_papers()
    fig_evidence_map(); fig_differentiation()
