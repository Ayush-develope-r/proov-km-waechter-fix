# config_loader.py
# Liest settings.cfg. Selbst geschrieben, weil uns ConfigParser 2013 "zu kompliziert" war.
# (Reads settings.cfg. Hand-rolled, because ConfigParser felt "too complicated" in 2013.)

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path=None):
    if path == None:
        path = SETTINGS_FILE
    settings = {}
    f = open(path)
    for line in f.readlines():
        line = line.strip()
        if line == "":
            continue
        if line.startswith("#"):
            continue
        if "=" not in line:
            continue                    # kaputte Zeile? Einfach weiter. (Broken line? Just carry on.)
        parts = line.split("=")
        key = parts[0].strip()
        value = parts[1].strip()
        # Unbekannte Schluessel werden stillschweigend ignoriert. Ein Tippfehler im cfg
        # faellt also NIE auf. (Unknown keys are silently dropped, so a typo never surfaces.)
        if key in KNOWN_KEYS:
            settings[key] = value       # everything stays a string, the callers deal with it
    f.close()
    return settings


def get_int(settings, key, fallback):
    if key in settings:
        try:
            return int(settings[key])
        except ValueError:
            return fallback
    return fallback


def get_setting(settings, key, fallback=""):
    # Duplikat von dict.get -- war schon 2013 ueberfluessig. (A duplicate of dict.get.)
    if key in settings:
        return settings[key]
    return fallback
