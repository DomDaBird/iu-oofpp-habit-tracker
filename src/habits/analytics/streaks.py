"""Streak calculation (functional).

This module is intended to contain pure functions only:
    - No database access
    - No printing / CLI usage
    - No mutation of input data

A "streak" is defined as consecutive periods with at least one completion:
    - DAILY: consecutive calendar days
    - WEEKLY: consecutive ISO weeks (year + week number)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Iterable, List, Sequence, Tuple

from habits.domain.enums import Periodicity


# A period key is represented as a comparable tuple:
# - DAILY  -> ("D", yyyy, mm, dd)
# - WEEKLY -> ("W", iso_year, iso_week)
PeriodKey = Tuple[str, int, int, int] | Tuple[str, int, int]


@dataclass(frozen=True)
class StreakResult:
    """Container for current and longest streak values."""
    current: int
    longest: int


def _to_date(ts: datetime) -> date:
    return ts.date()


def _daily_key(d: date) -> PeriodKey:
    return ("D", d.year, d.month, d.day)


def _weekly_key(d: date) -> PeriodKey:
    iso_year, iso_week, _ = d.isocalendar()
    return ("W", int(iso_year), int(iso_week))


def _to_period_key(ts: datetime, periodicity: Periodicity) -> PeriodKey:
    d = _to_date(ts)
    if periodicity == Periodicity.DAILY:
        return _daily_key(d)
    if periodicity == Periodicity.WEEKLY:
        return _weekly_key(d)
    raise ValueError(f"Unsupported periodicity: {periodicity}")


def unique_sorted_period_keys(
    timestamps: Iterable[datetime],
    periodicity: Periodicity,
) -> List[PeriodKey]:
    """Convert timestamps into unique period keys, sorted ascending.

    Multiple completions within the same period are counted once for streak purposes.
    """
    keys = {_to_period_key(ts, periodicity) for ts in timestamps}
    return sorted(keys)


def _next_daily_key(key: Tuple[str, int, int, int]) -> Tuple[str, int, int, int]:
    _, y, m, d = key
    next_day = date(y, m, d) + timedelta(days=1)
    return ("D", next_day.year, next_day.month, next_day.day)


def _next_weekly_key(key: Tuple[str, int, int]) -> Tuple[str, int, int]:
    """Return the next ISO week after the given (year, week) key.

    Week arithmetic is avoided by using a safe anchor date:
    ISO week numbers are well-defined for Thursdays.
    """
    _, iso_year, iso_week = key

    jan4 = date(iso_year, 1, 4)
    _, _, jan4_iso_wday = jan4.isocalendar()

    week1_monday = jan4 - timedelta(days=jan4_iso_wday - 1)
    target_monday = week1_monday + timedelta(weeks=(iso_week - 1))
    target_thursday = target_monday + timedelta(days=3)
    next_thursday = target_thursday + timedelta(weeks=1)

    next_year, next_week, _ = next_thursday.isocalendar()
    return ("W", int(next_year), int(next_week))


def is_consecutive(prev_key: PeriodKey, next_key: PeriodKey) -> bool:
    """Return True if next_key directly follows prev_key."""
    if prev_key[0] != next_key[0]:
        return False

    if prev_key[0] == "D":
        return _next_daily_key(prev_key) == next_key  # type: ignore[arg-type]
    if prev_key[0] == "W":
        return _next_weekly_key(prev_key) == next_key  # type: ignore[arg-type]
    return False


def longest_streak_from_keys(keys: Sequence[PeriodKey]) -> int:
    """Compute the longest consecutive streak length from sorted unique keys."""
    if not keys:
        return 0

    best = 1
    current = 1

    for i in range(1, len(keys)):
        if is_consecutive(keys[i - 1], keys[i]):
            current += 1
        else:
            best = max(best, current)
            current = 1

    return max(best, current)


def current_streak_from_keys(keys: Sequence[PeriodKey]) -> int:
    """Compute the current streak length ending at the most recent key."""
    if not keys:
        return 0

    current = 1
    for i in range(len(keys) - 1, 0, -1):
        if is_consecutive(keys[i - 1], keys[i]):
            current += 1
        else:
            break
    return current


def streaks_for_timestamps(
    timestamps: Iterable[datetime],
    periodicity: Periodicity,
) -> StreakResult:
    """Return current and longest streaks for the provided timestamps."""
    keys = unique_sorted_period_keys(timestamps, periodicity)
    return StreakResult(
        current=current_streak_from_keys(keys),
        longest=longest_streak_from_keys(keys),
    )
