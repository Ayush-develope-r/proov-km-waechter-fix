# log_util.py
# A homemade logger. The logging module felt like "too much magic" in 2013.

import time

LOG_LINES: list[str] = []   # module-level state; flush_log clears it
DEBUG: bool = False          # has been False since 2014; the debug branch is dead


def log(message: str) -> None:
    """Append a timestamped line to the in-memory log and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def debug(message: str) -> None:
    """Log a debug message — only active when DEBUG is True (currently always False)."""
    if DEBUG:
        log(f"DEBUG: {message}")


def flush_log(path: str) -> None:
    """Write all buffered log lines to the given file path, then clear the buffer."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
