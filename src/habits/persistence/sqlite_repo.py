"""SQLite repository implementation.

This module is intended to be the only place where sqlite3 and SQL statements are used.
All other layers are expected to depend on the HabitRepository interface.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from habits.domain.completion import Completion
from habits.domain.enums import Periodicity
from habits.domain.habit import Habit
from habits.persistence.repository import HabitRepository


def _dt_to_iso(dt: datetime) -> str:
    """Convert a datetime to an ISO 8601 string (UTC, timezone-aware)."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


def _iso_to_dt(value: str) -> datetime:
    """Parse an ISO 8601 datetime string."""
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


class SQLiteHabitRepository(HabitRepository):
    """SQLite-backed repository implementation."""

    def __init__(self, db_path: str | Path, schema_path: str | Path) -> None:
        self.db_path = str(db_path)
        self.schema_path = str(schema_path)

        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._apply_schema()

    def _apply_schema(self) -> None:
        with open(self.schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        self._conn.executescript(schema_sql)
        self._conn.commit()

    # ---------- Habit operations ----------

    def add_habit(self, habit: Habit) -> None:
        self._conn.execute(
            """
            INSERT INTO habits (id, name, periodicity, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (habit.id, habit.name, habit.periodicity.value, _dt_to_iso(habit.created_at)),
        )
        self._conn.commit()

    def remove_habit(self, habit_id: str) -> None:
        self._conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        self._conn.commit()

    def get_habit(self, habit_id: str) -> Optional[Habit]:
        row = self._conn.execute(
            "SELECT id, name, periodicity, created_at FROM habits WHERE id = ?",
            (habit_id,),
        ).fetchone()

        if row is None:
            return None

        habit = Habit(
            id=row["id"],
            name=row["name"],
            periodicity=Periodicity(row["periodicity"]),
            created_at=_iso_to_dt(row["created_at"]),
        )

        for c in self.list_completions(habit_id):
            habit.add_completion(c)

        return habit

    def list_habits(self) -> List[Habit]:
        rows = self._conn.execute(
            "SELECT id, name, periodicity, created_at FROM habits ORDER BY created_at ASC"
        ).fetchall()

        habits: List[Habit] = []
        for r in rows:
            habit = Habit(
                id=r["id"],
                name=r["name"],
                periodicity=Periodicity(r["periodicity"]),
                created_at=_iso_to_dt(r["created_at"]),
            )
            habits.append(habit)

        return habits

    # ---------- Completion operations ----------

    def add_completion(self, completion: Completion) -> None:
        self._conn.execute(
            """
            INSERT INTO completions (habit_id, timestamp, note)
            VALUES (?, ?, ?)
            """,
            (completion.habit_id, _dt_to_iso(completion.timestamp), completion.note),
        )
        self._conn.commit()

    def list_completions(self, habit_id: str) -> List[Completion]:
        rows = self._conn.execute(
            """
            SELECT habit_id, timestamp, note
            FROM completions
            WHERE habit_id = ?
            ORDER BY timestamp ASC
            """,
            (habit_id,),
        ).fetchall()

        return [
            Completion(
                habit_id=r["habit_id"],
                timestamp=_iso_to_dt(r["timestamp"]),
                note=r["note"],
            )
            for r in rows
        ]

    def list_all_completions(self) -> List[Completion]:
        rows = self._conn.execute(
            """
            SELECT habit_id, timestamp, note
            FROM completions
            ORDER BY timestamp ASC
            """
        ).fetchall()

        return [
            Completion(
                habit_id=r["habit_id"],
                timestamp=_iso_to_dt(r["timestamp"]),
                note=r["note"],
            )
            for r in rows
        ]

    def close(self) -> None:
        self._conn.close()
