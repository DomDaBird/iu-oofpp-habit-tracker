"""Completion domain model.

A completion event is represented as an immutable-like dataclass.
It is intended to be stored in an event-log style (append-only in persistence).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class Completion:
    """A single habit completion event.

    Attributes:
        habit_id: Identifier of the related habit
        timestamp: When the habit was completed (UTC, timezone-aware)
        note: Optional user note (used for sentiment analysis / UX feedback)
    """

    habit_id: str
    timestamp: datetime
    note: Optional[str] = None

    @classmethod
    def now(cls, habit_id: str, note: Optional[str] = None) -> "Completion":
        """Create a completion event with the current UTC timestamp."""
        return cls(
            habit_id=habit_id,
            timestamp=datetime.now(timezone.utc),
            note=note,
        )
