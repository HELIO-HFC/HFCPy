# SPDX-License-Identifier: EUPL-1.2
"""Write a shields.io endpoint badge (JSON) giving the total coverage of the tests.

Usage: python coverage_badge.py PERCENT OUTPUT_FILE

PERCENT is the total coverage, e.g. as given by ``coverage report --format=total``.
See https://shields.io/badges/endpoint-badge
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# (minimum coverage, color)
COLORS = ((90, "brightgreen"), (80, "green"), (70, "yellowgreen"), (60, "yellow"), (50, "orange"))


def badge(percent: float) -> dict[str, object]:
    """Return the shields.io endpoint badge of a coverage percentage."""
    color = next((color for minimum, color in COLORS if percent >= minimum), "red")
    return {"schemaVersion": 1, "label": "coverage", "message": f"{percent:.0f}%", "color": color}


def main(argv: list[str]) -> None:
    percent, output = float(argv[0]), Path(argv[1])
    output.write_text(json.dumps(badge(percent)) + "\n")
    print(f"Coverage badge: {percent:.0f}% -> {output}")


if __name__ == "__main__":
    main(sys.argv[1:])
