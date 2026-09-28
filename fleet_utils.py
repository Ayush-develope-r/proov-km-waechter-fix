# fleet_utils.py
# Catch-all helpers since 2013. Much of this is unused — never dared to delete anything.

KM_PER_MILE: float = 1.60934          # 1 mile = 1.60934 km
MILES_PER_KM: float = 1 / KM_PER_MILE  # 1 km ≈ 0.6214 miles  (was inverted: 1.609 — FIXED)


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles. Used by the nightly UK partner report."""
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a number as a whole-number percentage string."""
    return f"{int(value)}%"


def mean(values: list[float]) -> float:
    """Return the arithmetic mean of a list of numbers; 0 for an empty list.

    NOTE: statistics.mean() has existed since Python 3.4 — prefer that in new code.
    """
    if not values:
        return 0
    return sum(values) / len(values)


def is_due(pct: float, threshold: float) -> bool:
    """Return True if pct >= threshold.

    NOTE: Duplicates km_wachter.needs_service logic — kept for historical reference.
    """
    return pct >= threshold


def parse_service_date(text: str) -> tuple[int, int, int] | None:
    """Parse a DD.MM.YYYY date string into (year, month, day).

    NOTE: Was needed for the old garage form (2014). That form no longer exists.
    """
    parts = text.split(".")
    if len(parts) != 3:
        return None
    return (int(parts[2]), int(parts[1]), int(parts[0]))


def chunk_list(items: list, size: int) -> list[list]:
    """Split a list into chunks of the given size.

    NOTE: No longer called from anywhere (copied from Stack Overflow in 2013).
    """
    chunks = []
    current: list = []
    for item in items:
        current.append(item)
        if len(current) == size:
            chunks.append(current)
            current = []
    if current:
        chunks.append(current)
    return chunks
