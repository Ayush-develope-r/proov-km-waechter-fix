# config_loader.py
# Reads settings.cfg. Hand-rolled because ConfigParser felt "too complicated" in 2013.

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict[str, str]:
    """Read settings.cfg and return a dict of known key/value pairs (all values are strings)."""
    if path is None:
        path = SETTINGS_FILE
    settings: dict[str, str] = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            # Unknown keys are silently dropped — a typo in the cfg will never surface.
            if key in KNOWN_KEYS:
                settings[key] = value
    return settings


def get_int(settings: dict[str, str], key: str, fallback: int) -> int:
    """Return settings[key] as int, or fallback if the key is missing or not a valid int."""
    if key in settings:
        try:
            return int(settings[key])
        except ValueError:
            return fallback
    return fallback


def get_setting(settings: dict[str, str], key: str, fallback: str = "") -> str:
    """Return settings[key], or fallback if the key is absent.

    NOTE: This is equivalent to dict.get(key, fallback) — kept for compatibility.
    """
    return settings.get(key, fallback)
