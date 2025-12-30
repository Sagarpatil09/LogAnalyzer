"""Utility functions for parsing log lines."""
from datetime import datetime


def parse_log_line(line: str):
    parts = line.strip().split("\\t")

    timestamp, level, component, message = (
        parts[0],
        parts[1],
        parts[2],
        " ".join(parts[3:]),
    )

    return {
        "timestamp": datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
        "level": level,
        "component": component,
        "message": message,
    }
