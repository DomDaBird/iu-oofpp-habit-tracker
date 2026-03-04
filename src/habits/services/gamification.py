"""Gamification service.

A lightweight reward layer is implemented in this module:
    - XP points
    - Levels
    - Badges
    - Streak milestone bonuses

The core tracking logic is not intended to be modified by gamification.
The output is kept deterministic and test-friendly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set

from habits.analytics.streaks import StreakResult
from habits.domain.enums import Periodicity


@dataclass(frozen=True)
class GamificationResult:
    """Result returned after XP is awarded for a completion."""
    xp_gained: int
    new_total_xp: int
    new_level: int
    badges_earned: List[str]


XP_PER_LEVEL = 100


def level_from_xp(total_xp: int) -> int:
    """Convert total XP to a level number (starting at level 1)."""
    if total_xp < 0:
        raise ValueError("total_xp must be >= 0")
    return (total_xp // XP_PER_LEVEL) + 1


def base_xp_for_periodicity(periodicity: Periodicity) -> int:
    """Return base XP for a completion (weekly > daily)."""
    if periodicity == Periodicity.DAILY:
        return 10
    if periodicity == Periodicity.WEEKLY:
        return 25
    raise ValueError(f"Unsupported periodicity: {periodicity}")


def streak_bonus_xp(streak: StreakResult) -> int:
    """Return bonus XP for streak milestones (based on current streak)."""
    milestones = {3: 5, 7: 15, 14: 30, 30: 80}
    return milestones.get(streak.current, 0)


def derive_badges(
    *,
    periodicity: Periodicity,
    total_completions: int,
    streak: StreakResult,
    previously_earned: Set[str],
) -> List[str]:
    """Derive newly earned badges for the given completion context."""
    possible: List[str] = []

    if total_completions == 1:
        possible.append("First Step")

    if periodicity == Periodicity.DAILY and streak.current >= 7:
        possible.append("Daily Dynamo")
    if periodicity == Periodicity.WEEKLY and streak.current >= 4:
        possible.append("Weekly Warrior")

    if streak.current >= 3:
        possible.append("Streak Starter")
    if streak.current >= 14:
        possible.append("Two-Week Streak")
    if streak.current >= 30:
        possible.append("30-Day Legend")

    return [b for b in possible if b not in previously_earned]


class GamificationEngine:
    """In-memory gamification state.

    In this portfolio version, XP and earned badges are kept in memory.
    Persistence can be added later if desired.
    """

    def __init__(self) -> None:
        self._total_xp: int = 0
        self._badges: Set[str] = set()

    @property
    def total_xp(self) -> int:
        return self._total_xp

    @property
    def level(self) -> int:
        return level_from_xp(self._total_xp)

    @property
    def badges(self) -> Set[str]:
        return set(self._badges)

    def award_for_completion(
        self,
        *,
        periodicity: Periodicity,
        total_completions: int,
        streak: StreakResult,
    ) -> GamificationResult:
        """Award XP and badges for a completion."""
        gained = base_xp_for_periodicity(periodicity) + streak_bonus_xp(streak)

        new_badges = derive_badges(
            periodicity=periodicity,
            total_completions=total_completions,
            streak=streak,
            previously_earned=self._badges,
        )

        self._total_xp += gained
        for b in new_badges:
            self._badges.add(b)

        return GamificationResult(
            xp_gained=gained,
            new_total_xp=self._total_xp,
            new_level=self.level,
            badges_earned=new_badges,
        )
