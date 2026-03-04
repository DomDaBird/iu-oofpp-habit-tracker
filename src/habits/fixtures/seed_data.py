"""Seed / demo data for the habit tracker.

This module is intended to provide:
    - quick manual testing data
    - CLI demos
    - predictable example data (4-week fixtures)

Direct interaction with CLI or persistence is intentionally avoided.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from habits.domain.completion import Completion
from habits.domain.enums import Periodicity
from habits.domain.habit import Habit


def create_demo_habits() -> List[Habit]:
    """Create and return a small set of predefined habits (3 daily, 2 weekly)."""
    return [
        Habit(name="Drink Water", periodicity=Periodicity.DAILY),
        Habit(name="Read 10 Pages", periodicity=Periodicity.DAILY),
        Habit(name="Workout", periodicity=Periodicity.DAILY),
        Habit(name="Weekly Review", periodicity=Periodicity.WEEKLY),
        Habit(name="Call Family", periodicity=Periodicity.WEEKLY),
    ]


def generate_completions(
    habit: Habit,
    *,
    days_back: int,
    every_n_days: int = 1,
    note: Optional[str] = None,
    now: Optional[datetime] = None,
) -> None:
    """Generate synthetic completion history for a habit.

    Example:
        generate_completions(habit, days_back=14, every_n_days=1)
        -> daily completions for the last 14 days

    Determinism note:
        When a fixed `now` is provided, reproducible fixtures are produced.
    """
    anchor = now or datetime.now(timezone.utc)

    for i in range(0, days_back, every_n_days):
        ts = anchor - timedelta(days=i)
        completion = Completion(habit_id=habit.id, timestamp=ts, note=note)
        habit.add_completion(completion)


def populate_demo_data(habits: List[Habit]) -> None:
    """Populate demo habits with realistic completion patterns (4 weeks)."""
    anchor = datetime.now(timezone.utc)

    for habit in habits:
        if habit.periodicity == Periodicity.DAILY:
            generate_completions(
                habit,
                days_back=28,
                every_n_days=1,
                note="felt good and motivated",
                now=anchor,
            )
        elif habit.periodicity == Periodicity.WEEKLY:
            generate_completions(
                habit,
                days_back=28,
                every_n_days=7,
                note="hard but important",
                now=anchor,
            )
        else:
            raise ValueError(f"Unsupported periodicity: {habit.periodicity}")
