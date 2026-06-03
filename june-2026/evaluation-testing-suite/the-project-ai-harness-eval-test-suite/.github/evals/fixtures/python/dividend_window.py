"""Small controlled fixture for AI-harness code-edit evals.

The bug is intentional. The expected behavior is described in
`test_dividend_window.py`. This fixture is independent of production the project code.
"""

from __future__ import annotations

from datetime import date


def days_to_ex_date(today: date, ex_date: date) -> int:
    """Return positive days from today until ex-date.

    Examples:
    - today=2026-06-01, ex_date=2026-06-10 => 9
    - today=2026-06-10, ex_date=2026-06-10 => 0
    - today=2026-06-12, ex_date=2026-06-10 => -2
    """
    # BUG: absolute value loses whether ex-date is in the past.
    return abs((ex_date - today).days)


def is_inside_capture_window(today: date, ex_date: date, days_before: int, days_after: int) -> bool:
    """Return whether `today` is inside [ex_date-days_before, ex_date+days_after]."""
    offset = days_to_ex_date(today, ex_date)
    return -days_after <= offset <= days_before


def classify_capture_timing(today: date, ex_date: date) -> str:
    """Classify timing relative to ex-date for a simple smoke test."""
    offset = days_to_ex_date(today, ex_date)
    if offset > 0:
        return "before"
    if offset == 0:
        return "ex-date"
    return "after"
