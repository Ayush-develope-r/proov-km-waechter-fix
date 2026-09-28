# verify.py
# Your acceptance check. Run this before you hand the repo in:  python verify.py
#
# It does not grade you. It tells you, honestly, whether the job is actually done — so that
# "finished" is something you checked, not something the AI told you.

import os

import km_wachter as km
import fleet_report as fr

checks = []


def check(name, fn):
    try:
        ok, detail = fn()
    except Exception as e:
        ok, detail = False, "raised %s: %s" % (type(e).__name__, e)
    checks.append((name, ok, detail))


def wear_is_not_floored():
    pct = km.wear_percent(14900, 15000)
    return (98 <= pct <= 100), "a car at 14,900 of 15,000 km reports %.1f%% (should be about 99.3%%)" % pct


def nearly_worn_car_is_flagged():
    flagged = km.needs_service({"id": "VOS-4471", "odometer": 14900, "last_service_km": 0})
    return flagged is True, "the nearly-worn car is %s" % ("flagged" if flagged else "NOT flagged")


def missing_reading_is_handled():
    flagged = km.needs_service({"id": "VOS-7788", "odometer": 92000})
    return flagged is False, "a car with no last-service reading is %s" % ("wrongly flagged" if flagged else "handled")


def rules_are_unchanged():
    ok = km.SERVICE_INTERVAL_KM == 15000 and km.WARN_AT_PERCENT == 80
    return ok, "interval=%s, threshold=%s (both must be untouched)" % (km.SERVICE_INTERVAL_KM, km.WARN_AT_PERCENT)


def config_rules_are_unchanged():
    from config_loader import load_settings, get_int
    s = load_settings()
    interval = get_int(s, "service_interval_km", -1)
    warn = get_int(s, "warn_at_percent", -1)
    ok = interval == 15000 and warn == 80
    return ok, "settings.cfg says interval=%s, threshold=%s (both must be untouched)" % (interval, warn)


def mileage_conversion_is_fixed():
    import fleet_utils
    miles = fleet_utils.km_to_miles(100)
    return (61.0 <= miles <= 63.5), "100 km reads as %.1f miles (should be about 62.1)" % miles


def report_survives_a_missing_reading():
    fleet = [
        {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
        {"id": "VOS-7788", "odometer": 92000},
    ]
    s = fr.fleet_summary(fleet)
    return "average_wear" in s, "the nightly report ran without crashing: %s" % s


def average_is_not_floored():
    fleet = [
        {"id": "A", "odometer": 14900, "last_service_km": 0},
        {"id": "B", "odometer": 3000, "last_service_km": 0},
    ]
    avg = fr.fleet_summary(fleet)["average_wear"]
    return abs(avg - 59.67) < 1.5, "average wear reads %.2f (should be about 59.67)" % avg


def you_added_the_missing_test():
    if not os.path.exists("test_fleet_report.py"):
        return False, "test_fleet_report.py is missing"
    body = open("test_fleet_report.py").read()
    added = body.count("def test_") >= 2
    return added, "test_fleet_report.py holds %d test(s); it needs the missing-reading one too" % body.count("def test_")


def you_did_the_risk_analysis():
    if not os.path.exists("analyze.py"):
        return False, "analyze.py is missing"
    body = open("analyze.py").read()
    done = "your analysis here" not in body and len(body) > 700
    return done, "analyze.py looks %s" % ("written" if done else "unfinished")


def you_wrote_your_notes():
    if not os.path.exists("NOTES.md"):
        return False, "NOTES.md is missing — write what the agent got wrong that you caught"
    body = open("NOTES.md").read()
    # Length alone proves nothing: the template we ship is already long. What proves you wrote it
    # is that the prompts in brackets are GONE, because you answered them.
    untouched = "(Every agent gets something wrong" in body or "(How do you KNOW" in body
    if untouched:
        return False, "NOTES.md is still the blank template — answer the questions in it, in your own words"
    return len(body.strip()) >= 250, "NOTES.md is %d characters (needs real paragraphs, not one line)" % len(body.strip())


check("Wear is no longer floored to 0", wear_is_not_floored)
check("The nearly-worn car is flagged", nearly_worn_car_is_flagged)
check("A missing reading is handled", missing_reading_is_handled)
check("The 15000 km / 80% rules are untouched", rules_are_unchanged)
check("The settings.cfg rules are untouched", config_rules_are_unchanged)
check("The nightly report no longer crashes", report_survives_a_missing_reading)
check("The average wear is correct", average_is_not_floored)
check("The km-to-miles conversion is fixed", mileage_conversion_is_fixed)
check("You added the missing test", you_added_the_missing_test)
check("You did the breakdown-risk analysis", you_did_the_risk_analysis)
check("You wrote NOTES.md in your own words", you_wrote_your_notes)

print("")
print("KM-Waechter acceptance check")
print("=" * 60)
passed = 0
for name, ok, detail in checks:
    print("%s  %s" % ("PASS " if ok else "FAIL ", name))
    print("        %s" % detail)
    if ok:
        passed += 1
print("=" * 60)
print("%d of %d checks pass." % (passed, len(checks)))
if passed == len(checks):
    print("Done. Push it and hand in the link.")
else:
    print("Not done yet. Fix the FAILs above, then run me again.")
