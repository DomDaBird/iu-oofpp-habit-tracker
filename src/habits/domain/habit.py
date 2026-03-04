"""Habit domain model.

The core concept of a habit is encoded as a class using object-oriented programming.
Business rules related to completions are encapsulated in this class.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from habits.domain.completion import Completion
from habits.domain.enums import Periodicity


@dataclass
class Habit:
    """A habit tracked by the user.

    Responsibilities:
        - Habit metadata is stored (name, periodicity, created_at)
        - Completion events are accepted and validated
        - Completion history is exposed read-only
    """

    name: str
    periodicity: Periodicity
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    _completions: List[Completion] = field(default_factory=list, repr=False)

    def add_completion(self, completion: Completion) -> None:
        """Attach a completion to this habit.

        Validation:
            - The completion must belong to this habit (matching habit_id)
        """
        if completion.habit_id != self.id:
            raise ValueError("Completion habit_id does not match this habit.")

        self._completions.append(completion)

    @property
    def completions(self) -> List[Completion]:
        """Return a copy of completion history (to protect internal state)."""
        return list(self._completions)

    def total_completions(self) -> int:
        """Return the total number of recorded completion events."""
        return len(self._completions)

    def __str__(self) -> str:
        return f"Habit(name='{self.name}', periodicity={self.periodicity.value})"
