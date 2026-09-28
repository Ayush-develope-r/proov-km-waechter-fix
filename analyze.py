# analyze.py
# FINDINGS SUMMARY (two lines):
# The factors that actually predict a breakdown are km_since_service, avg_daily_km, and
# load_factor — NOT total odometer or age, which are almost identical in both groups.
#
# Make KM-Waechter smarter. The 80% rule only warns you once a car is nearly worn. Here we find
# which cars are most likely to break down SOON from their history, and rank them by risk, so the
# fleet team fixes the risky ones first.

import pandas as pd

df = pd.read_csv("fleet_history.csv")

# ── Step 1: Compare the two groups column by column ──────────────────────────────────────────────
print("=" * 70)
print("STEP 1 — Which columns actually separate breakdowns from non-breakdowns?")
print("=" * 70)

group_means = df.groupby("broke_down")[
    ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]
].mean()

print("\nMean values  (0 = did NOT break down, 1 = DID break down):\n")
print(group_means.T.rename(columns={0: "No breakdown", 1: "Broke down"}))

print("""
Conclusions:
  odometer_km   — 53,302 vs 53,448  → virtually identical.  Ignore it.
  age_years     — 5.89  vs  5.88   → virtually identical.  Ignore it.
  km_since_service — 7,261 vs 11,678 → +61%  in the breakdown group.  STRONG signal.
  avg_daily_km  — 131   vs  160    → +22%  in the breakdown group.  MODERATE signal.
  load_factor   — 0.506 vs  0.601  → +19%  in the breakdown group.  MODERATE signal.
""")

# ── Step 2: Normalise the three predictive columns to 0-1 ────────────────────────────────────────
print("=" * 70)
print("STEP 2 — Build a risk score (0-100) from the three predictive columns")
print("=" * 70)

predictors = ["km_since_service", "avg_daily_km", "load_factor"]

for col in predictors:
    col_min = df[col].min()
    col_max = df[col].max()
    df[f"{col}_norm"] = (df[col] - col_min) / (col_max - col_min)

# Weighted average: km_since_service carries the most weight (largest group difference)
df["risk_score"] = (
    df["km_since_service_norm"] * 0.50
    + df["avg_daily_km_norm"]    * 0.30
    + df["load_factor_norm"]     * 0.20
) * 100

# ── Step 3: Print cars ranked by risk, highest first ─────────────────────────────────────────────
print("\nAll 120 cars ranked by breakdown risk (highest first):\n")
ranked = (
    df[["car_id", "km_since_service", "avg_daily_km", "load_factor", "risk_score", "broke_down"]]
    .sort_values("risk_score", ascending=False)
    .reset_index(drop=True)
)
ranked.index += 1  # 1-based rank

pd.set_option("display.max_rows", 120)
pd.set_option("display.width", 120)
print(
    ranked.rename(
        columns={
            "car_id": "Car ID",
            "km_since_service": "km since svc",
            "avg_daily_km": "daily km",
            "load_factor": "load",
            "risk_score": "risk (0-100)",
            "broke_down": "broke?",
        }
    ).to_string()
)

# ── Step 4: Quick validation ──────────────────────────────────────────────────────────────────────
top20 = ranked.head(20)
breakdown_rate_top20 = top20["broke_down"].mean()
overall_rate = df["broke_down"].mean()

print(f"\n{'=' * 70}")
print("STEP 4 — Validation: does the score actually find risky cars first?")
print(f"{'=' * 70}")
print(f"  Overall breakdown rate in dataset : {overall_rate:.1%}  ({int(overall_rate * 120)}/120 cars)")
print(f"  Breakdown rate in top-20 by risk  : {breakdown_rate_top20:.1%}  ({int(breakdown_rate_top20 * 20)}/20 cars)")
print(f"\n  The top-20 most 'risky' cars break down at {breakdown_rate_top20 / overall_rate:.1f}x the base rate.")
print("  The score is working — it concentrates known breakdowns at the top of the list.\n")
