# Your mission — fix and modernize KM-Waechter

You are a junior engineer at Vossberg Mobility. This repo decides when 6,000 sports cars get
serviced and prints the nightly health report. It is broken, the code is dated, and — like every
real inherited code base — it is bigger than the bug list. Part of the job is finding out which
files matter.

Do this with IBM Bob. You do NOT need the Proov tab open while you work. Everything you need is
in this file. Come back when the repo is green.

## You do not need to set anything up
You do not need Python installed. You do not need to know pytest or pandas. Your agent runs the
code, runs the tests, and can push to GitHub for you. Your job is to DIRECT it and to CHECK it —
that is the actual skill here, and it is the one being graded.

## What to do
1. Have Bob READ the repo first. Before any change, ask it to read every file and tell you what
   the service does, how the files depend on each other, and why each test fails. Correct it if
   its summary is wrong — it works for you.
2. Run the tests. Several fail. Read why each one fails.
3. Fix the wear bug in km_wachter.py so a nearly-worn car is flagged.
4. Fix the missing-reading bug so a car with no last-service reading is not falsely flagged.
5. Fix fleet_report.py: it crashes on a car with no reading, and its average wear is wrong.
6. Have Bob ADD the missing test noted in test_fleet_report.py (a car with no reading must not
   crash the report), and make it pass.
7. Sweep the helper files (config_loader.py, fleet_utils.py, log_util.py). They carry the same
   dated style, dead code that nobody dared to delete, and at least ONE more quiet bug that no
   test catches. Have Bob tell you what it found BEFORE it fixes anything, then decide together
   what to fix and what to delete.
8. Modernize the style across the files you touched: f-strings, type hints, short docstrings,
   and remove the "== True" comparisons and the needless else.
9. Make it smarter (this is the part you show off). Open analyze.py. With Bob and pandas, use
   fleet_history.csv (120 cars, and we know which ones later broke down) to find which factors
   actually predict a breakdown, then print a risk score for each car so the team fixes the risky
   ones BEFORE the 80 percent rule would ever flag them.

   Be careful here. The obvious column is total mileage. Check whether it actually separates the
   cars that broke down from the ones that did not — a lot of juniors report "older, higher-mileage
   cars break down" and the data does not say that. Follow the data, not the assumption.

10. Write NOTES.md: in your own words, what did the agent get WRONG that you caught? Every agent
    gets something wrong on a job this size. If you genuinely caught nothing, say what you checked
    and how you convinced yourself it was right.

## Do not change
- The 15000 km service interval.
- The 80 percent flag threshold.
- The rule values in settings.cfg (they must keep matching the code).
- What the service is meant to decide.

## Done when
Run your own acceptance check:

```
python verify.py
```

It prints PASS or FAIL for each requirement. Do not hand in until it is all PASS. That is the
difference between "the AI said it was finished" and "I checked".

## About your free trial
The whole mission is about 10 to 14 agent prompts, and the free Bob trial gives you 40 Bobcoins,
which is comfortably more than the job needs (trial terms as at the time of writing, and they can
change). If you cannot use Bob at all, any AI coding agent can do the job — and if you run low on
prompts, finish the remaining steps by hand. The skill being graded is directing and checking,
not which tool you used.

## Hand it back
Commit and push everything to the repository you created from our template, then paste its link
into Proov. Bob can do it for you — ask it: "commit every change with a clear message and push to
my GitHub repository, then give me the repository link."
