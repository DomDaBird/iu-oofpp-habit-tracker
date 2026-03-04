"""Domain enums used across the habit tracker.

This module is intended to remain dependency-free and stable, because it is imported
by many other modules. Values are stored as strings to simplify persistence and CLI input.
"""

from __future__ import annotations

from enum import Enum


class Periodicity(str, Enum):
    """Periodicity for a habit (daily or weekly)."""

    DAILY = "daily"
    WEEKLY = "weekly"

    @classmethod
    def from_user_input(cls, value: str) -> "Periodicity":
        """Parse common user inputs into a periodicity value.

        Examples:
            "daily", "d", "day"    -> Periodicity.DAILY
            "weekly", "w", "week"  -> Periodicity.WEEKLY
        """
        if value is None:
            raise ValueError("Periodicity input must not be None.")

        normalized = value.strip().lower()

        daily_aliases = {"daily", "day", "d", "1"}
        weekly_aliases = {"weekly", "week", "w", "7"}

        if normalized in daily_aliases:
            return cls.DAILY
        if normalized in weekly_aliases:
            return cls.WEEKLY

        raise ValueError(
            f"Unsupported periodicity: '{value}'. Use 'daily' or 'weekly'."
        )
