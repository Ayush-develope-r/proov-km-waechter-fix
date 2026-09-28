# What I checked, and what the agent got wrong

## What the agent got wrong

When I first asked the agent to analyse the helper files it correctly spotted the inverted
`MILES_PER_KM` constant, but it initially described the fix as "change 1.609 to 0.621" — a bare
magic number with no explanation of where 0.621 came from. I pushed back and asked it to express
the fix as `1 / KM_PER_MILE` so the relationship is self-documenting. It also left the broken
`parse_service_date` and `chunk_list` functions in place with only a comment — I confirmed that was
acceptable because they are not called anywhere, but I made sure to check that myself before
agreeing.

## What I checked before I accepted its work

- I read the two rule constants in `km_wachter.py` by eye: `SERVICE_INTERVAL_KM = 15000` and
  `WARN_AT_PERCENT = 80`. Neither changed.
- I read `settings.cfg` by eye: `service_interval_km = 15000` and `warn_at_percent = 80`.
  Neither changed.
- I ran `python verify.py` and read every PASS line. The checks "The 15000 km / 80% rules are
  untouched" and "The settings.cfg rules are untouched" both passed, which confirmed the agent
  had not silently altered the thresholds.
- I ran pytest and watched all four tests go green one by one.
- I manually checked that `km_to_miles(100)` now returns 62.1 (not 160.9), matching the
  verify.py output.

## What the data actually said

The obvious assumption — that high total mileage and older age predict breakdowns — turned out to
be wrong. In `fleet_history.csv`, the average odometer reading for cars that broke down (53,448 km)
is almost identical to cars that did not (53,302 km). Age is the same: 5.88 years versus 5.89.
Neither column separates the two groups at all.

What actually separates them is how hard the car has been worked recently:

- **km_since_service**: cars that broke down had an average of 11,678 km since their last service
  versus 7,261 km for cars that did not — a 61 % difference. This is by far the strongest signal.
- **avg_daily_km**: breakdown cars averaged 160 daily km versus 131 — about 22 % higher.
- **load_factor**: breakdown cars had a load factor of 0.60 versus 0.51 — about 19 % higher.

The risk score weights these three columns (50 / 30 / 20) and ignores odometer and age entirely.
The top-20 highest-risk cars in the dataset break down at roughly 2-3x the base rate, confirming
the score is genuinely predictive rather than random.
