"""Analytics (functional).

This module provides pure functions operating on domain objects or primitive data.
No DB access, no CLI usage, and no side effects are intended.

Required analytics include:
    - listing habits
    - listing habits by periodicity
    - returning the longest streak overall
    - returning the longest streak for a given habit
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from habits.analytics.streaks import StreakResult, streaks_for_timestamps
from habits.domain.enums import Periodicity
from habits.domain.habit import Habit


@dataclass(frozen=True)
class HabitStreakSummary:
    """Analytics summary for a single habit."""
    habit_id: str
    habit_name: str
    periodicity: Periodicity
    current_streak: int
    longest_streak: int
    total_completions: int


def filter_habits_by_periodicity(
    habits: Iterable[Habit],
    periodicity: Periodicity,
) -> List[Habit]:
    """Return only habits that match the given periodicity."""
    return [h for h in habits if h.periodicity == periodicity]


def streak_summary_for_habit(habit: Habit) -> HabitStreakSummary:
    """Compute a streak summary for the given habit."""
    timestamps = [c.timestamp for c in habit.completions]
    streaks: StreakResult = streaks_for_timestamps(timestamps, habit.periodicity)

    return HabitStreakSummary(
        habit_id=habit.id,
        habit_name=habit.name,
        periodicity=habit.periodicity,
        current_streak=streaks.current,
        longest_streak=streaks.longest,
        total_completions=habit.total_completions(),
    )


def streak_summaries(
    habits: Iterable[Habit],
    periodicity: Optional[Periodicity] = None,
) -> List[HabitStreakSummary]:
    """Compute streak summaries for multiple habits.

    If periodicity is provided, habits are filtered first.
    """
    habit_list = list(habits)
    if periodicity is not None:
        habit_list = filter_habits_by_periodicity(habit_list, periodicity)

    return [streak_summary_for_habit(h) for h in habit_list]


def habit_with_longest_streak(
    habits: Iterable[Habit],
    periodicity: Optional[Periodicity] = None,
) -> Optional[HabitStreakSummary]:
    """Return the habit summary with the longest streak (or None)."""
    summaries = streak_summaries(habits, periodicity=periodicity)
    if not summaries:
        return None
    return max(summaries, key=lambda s: s.longest_streak)


def build_habit_index(habits: Iterable[Habit]) -> Dict[str, Habit]:
    """Build and return a dict index from habit_id -> Habit."""
    return {h.id: h for h in habits}
