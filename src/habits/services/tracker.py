"""HabitTracker service.

This is the central application service where orchestration is performed:
    - domain models (Habit, Completion)
    - persistence (HabitRepository)
    - analytics (functional streak calculations)
    - gamification (XP, levels, badges)
    - sentiment feedback (UX)

The CLI is expected to communicate only with this service.
"""

from __future__ import annotations

from typing import List, Optional, Dict, Any

from habits.analytics.analytics import (
    HabitStreakSummary,
    habit_with_longest_streak,
    streak_summary_for_habit,
)
from habits.analytics.streaks import StreakResult, streaks_for_timestamps
from habits.domain.completion import Completion
from habits.domain.enums import Periodicity
from habits.domain.habit import Habit
from habits.persistence.repository import HabitRepository
from habits.services.gamification import GamificationEngine, GamificationResult
from habits.ux.sentiment import SentimentResult, feedback_message, score_sentiment


class HabitTracker:
    """High-level application service."""

    def __init__(self, repository: HabitRepository) -> None:
        self._repo = repository
        self._gamification = GamificationEngine()

    # ---------- Habit management ----------

    def create_habit(self, name: str, periodicity: Periodicity) -> Habit:
        habit = Habit(name=name, periodicity=periodicity)
        self._repo.add_habit(habit)
        return habit

    def delete_habit(self, habit_id: str) -> None:
        self._repo.remove_habit(habit_id)

    def list_habits(self) -> List[Habit]:
        return self._repo.list_habits()

    def get_habit(self, habit_id: str) -> Optional[Habit]:
        return self._repo.get_habit(habit_id)

    # ---------- Completion handling ----------

    def complete_habit(self, habit_id: str, note: Optional[str] = None) -> Dict[str, Any]:
        """Mark a habit as completed and return a UX-friendly result."""
        habit = self._repo.get_habit(habit_id)
        if habit is None:
            raise ValueError(f"Habit with id '{habit_id}' not found.")

        completion = Completion.now(habit_id=habit.id, note=note)
        habit.add_completion(completion)
        self._repo.add_completion(completion)

        timestamps = [c.timestamp for c in habit.completions]
        streak: StreakResult = streaks_for_timestamps(timestamps, habit.periodicity)

        gamification: GamificationResult = self._gamification.award_for_completion(
            periodicity=habit.periodicity,
            total_completions=habit.total_completions(),
            streak=streak,
        )

        sentiment: SentimentResult = score_sentiment(note)
        sentiment_text: str = feedback_message(sentiment)

        return {
            "habit": habit,
            "streak": streak,
            "gamification": gamification,
            "sentiment": sentiment,
            "sentiment_feedback": sentiment_text,
        }

    # ---------- Analytics ----------

    def streak_summary(self, habit_id: str) -> HabitStreakSummary:
        habit = self._repo.get_habit(habit_id)
        if habit is None:
            raise ValueError(f"Habit with id '{habit_id}' not found.")
        return streak_summary_for_habit(habit)

    def longest_streak(self) -> Optional[HabitStreakSummary]:
        # Full habits are loaded so that completions are available for analytics.
        full_habits: List[Habit] = []
        for h in self._repo.list_habits():
            full = self._repo.get_habit(h.id)
            if full is not None:
                full_habits.append(full)
        return habit_with_longest_streak(full_habits)

    # ---------- Shutdown ----------

    def close(self) -> None:
        self._repo.close()
