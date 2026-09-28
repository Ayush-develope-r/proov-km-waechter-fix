# What I checked, and what the agent got wrong

## Overview of the task

I was given a broken Python service called KM-Wächter, which is used by a fictional car-rental
company (Vossberg Mobility) to decide when each car in a 6,000-car fleet needs a service. The
service had hidden bugs, failing tests, and code written in an old style back in 2013-2014 that
nobody had cleaned up since. My job was to direct IBM Bob to fix and modernise it — while making
sure it never changed the core business rules (15,000 km service interval, 80% warning threshold).

---

## Every change that was made, and why

### km_wachter.py — the core decision engine

**Bug 1 — floor division in wear_percent:**
The original code used `//` (integer/floor division) to calculate how worn a car is:
```python
ratio = km_since_service // interval
return ratio * 100
```
This meant a car at 14,900 km out of a 15,000 km window (99.3% worn) reported **0%** because
`14900 // 15000 = 0`. The fix was to switch to true division `/`:
```python
return (km_since_service / interval) * 100
```
Now the same car correctly reports 99.3% and gets flagged.

**Bug 2 — missing last_service_km defaulted to 0:**
If a car had no `last_service_km` reading in its data, the original code assumed it was serviced
at odometer 0 and calculated wear from there. A car at 92,000 km with no reading was treated as
having 6+ service intervals of wear and wrongly flagged as urgent. The fix: if the key is missing,
return `False` immediately — we don't know the history, so we don't flag it.

**Style:** Removed `if needs_service(car) == True:` (comparing a boolean to True with `==` is
redundant). Added type hints and docstrings throughout.

---

### fleet_report.py — the nightly health report

**Bug 3 — crash on missing last_service_km:**
`car_wear()` did `car["last_service_km"]` — a direct dictionary lookup that raises a `KeyError`
if the key is absent. Changed to `car.get("last_service_km")` with a `None` check, returning
0.0 wear for cars with no reading instead of crashing the whole report.

**Bug 4 — integer division for the fleet average:**
`average = total // len(fleet)` used floor division again, silently dropping the decimal part.
Changed to `total / len(fleet)` so the average is accurate (e.g. 59.67% instead of 59%).

**Style:** Replaced `% `string formatting with f-strings, replaced the manual `for` loop over
`total_km` with `sum()`, added type hints and docstrings, removed `== True` comparison.

---

### fleet_utils.py — the helper utilities

**Bug 5 — MILES_PER_KM was inverted (the silent wrong number):**
The constant was set to `1.609`, but that is how many km are in a mile — the wrong way round.
`km_to_miles(100)` returned **160.9 miles** instead of 62.1. The fix:
```python
KM_PER_MILE: float = 1.60934
MILES_PER_KM: float = 1 / KM_PER_MILE   # ≈ 0.6214
```
This also makes the relationship self-documenting — you can see exactly why the number is what
it is. No test caught this; only `verify.py` checked it.

**Style:** Added type hints and docstrings to all functions. Kept the dead-code functions
(`parse_service_date`, `chunk_list`, `is_due`, `mean`) but added clear notes explaining they are
unused, because removing them was not part of the task and they do no harm.

---

### config_loader.py — the settings file reader

Three quiet problems fixed:
- `if path == None:` changed to `if path is None:` — the correct Python way to check for None.
- `f = open(path)` without a `with` statement — if an exception happened mid-read, the file
  handle would never be closed. Changed to `with open(path) as f:`.
- `line.split("=")` changed to `line.partition("=")` — `split` would break any setting whose
  value contained an `=` sign; `partition` only splits on the first one.

Type hints and docstrings added throughout.

---

### log_util.py — the homemade logger

Three quiet problems fixed:
- `flush_log` opened a file without `with` — same file-leak risk as config_loader.
- `del LOG_LINES[:]` changed to `LOG_LINES.clear()` — `.clear()` is the modern Python 3 idiom.
- `if DEBUG == True:` changed to `if DEBUG:` — comparing a boolean to True with `==` is
  redundant.

Type hints and docstrings added. The `DEBUG = False` branch is still dead code (it has been since
2014, per the original comment), but it was left in place since removing it was not asked for.

---

### test_fleet_report.py — the test suite

Added the missing test that was noted in a TODO comment at the bottom of the file:
`test_summary_does_not_crash_on_missing_reading`. It passes a fleet that includes a car with no
`last_service_km` key and asserts that `fleet_summary` runs without crashing and still counts
the `due` cars correctly.

---

### analyze.py — the breakdown-risk analysis (the capstone)

Wrote a full data-driven analysis using pandas against `fleet_history.csv` (120 cars, each
labelled with whether it later broke down).

The approach: compare the mean of every column between the two groups (broke down vs did not).
This is the key finding — see the section below for details. From the three columns that actually
separated the groups, I built a simple weighted risk score from 0 to 100 for each car and printed
all 120 cars ranked by risk, highest first.

---

## What the agent got wrong

The agent initially described the `MILES_PER_KM` fix as "change 1.609 to 0.621" — a bare magic
number dropped into the code with no explanation of where it came from. I pushed back and asked
it to write the fix as `1 / KM_PER_MILE` instead, so anyone reading the code in the future can
see the reasoning. That is the kind of thing an AI agent misses: it gets the number right but
loses the self-documentation. I also made sure to check that the two business-rule constants
(`SERVICE_INTERVAL_KM = 15000` and `WARN_AT_PERCENT = 80`) were never touched — I read them by
eye in the file and confirmed them with `verify.py` before accepting the work.

---

## What I checked before I accepted the work

- Read `km_wachter.py` by eye: `SERVICE_INTERVAL_KM = 15000`, `WARN_AT_PERCENT = 80`. Untouched.
- Read `settings.cfg` by eye: same two values. Untouched.
- Ran `python -m pytest -v` and watched all four tests turn green one by one.
- Ran `python verify.py` and read every single PASS line before calling it done.
- Specifically confirmed the miles conversion: `km_to_miles(100)` now returns 62.1, not 160.9.

---

## What the data actually said

The obvious assumption going in was: high total mileage and older cars break down more. The data
does not say that. In `fleet_history.csv`, the average odometer reading for cars that broke down
is 53,448 km — almost identical to 53,302 km for cars that did not. Average age is 5.88 years
versus 5.89. Neither column separates the two groups at all.

What actually separates them is how hard the car has been worked recently:

- **km_since_service** — cars that broke down averaged 11,678 km since their last service;
  cars that did not averaged 7,261 km. That is a 61% difference and by far the strongest signal.
- **avg_daily_km** — breakdown cars averaged 160 daily km vs 131 for healthy cars (+22%).
- **load_factor** — breakdown cars had a load factor of 0.60 vs 0.51 (+19%).

The risk score weights these three columns 50/30/20 and ignores odometer and age entirely. As a
sanity check: the top-20 highest-risk cars in the dataset break down at about 2-3x the overall
base rate of 21.7%, which confirms the score is genuinely finding risky cars rather than just
picking randomly.

The practical takeaway: a car that has been driven hard and long since its last service is a
much better target for early attention than a car that simply has high total mileage or is old.
