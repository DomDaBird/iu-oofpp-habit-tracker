"""Persistence repository abstractions.

The repository contract is defined in this module.
Concrete implementations (e.g., SQLite) are expected to follow this API.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from habits.domain.completion import Completion
from habits.domain.habit import Habit


class HabitRepository(ABC):
    """Abstract repository interface for habits and completions."""

    @abstractmethod
    def add_habit(self, habit: Habit) -> None:
        """Persist the given habit."""
        raise NotImplementedError

    @abstractmethod
    def remove_habit(self, habit_id: str) -> None:
        """Remove a habit by id."""
        raise NotImplementedError

    @abstractmethod
    def get_habit(self, habit_id: str) -> Optional[Habit]:
        """Return the habit (including completions) or None."""
        raise NotImplementedError

    @abstractmethod
    def list_habits(self) -> List[Habit]:
        """Return a list of all habits (metadata only)."""
        raise NotImplementedError

    @abstractmethod
    def add_completion(self, completion: Completion) -> None:
        """Persist a completion event."""
        raise NotImplementedError

    @abstractmethod
    def list_completions(self, habit_id: str) -> List[Completion]:
        """Return all completions for a habit."""
        raise NotImplementedError

    @abstractmethod
    def list_all_completions(self) -> List[Completion]:
        """Return all completions across all habits."""
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """Close underlying resources (e.g., DB connection)."""
        raise NotImplementedError
