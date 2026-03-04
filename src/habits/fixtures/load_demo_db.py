"""Load demo habits and 4-week demo completion data into a SQLite database.

The script is intended to provide a repeatable way to create a demo database for:
    - manual evaluation by the tutor
    - CLI demonstrations
    - screenshots

Usage (from project root):
    python -m habits.fixtures.load_demo_db --reset
"""

from __future__ import annotations

import argparse
from pathlib import Path

from habits.fixtures.seed_data import create_demo_habits, populate_demo_data
from habits.persistence.sqlite_repo import SQLiteHabitRepository


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load demo data into SQLite DB.")
    parser.add_argument(
        "--db",
        default="habits.db",
        help="Path to SQLite database file (default: habits.db).",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete existing DB file before loading demo data.",
    )
    return parser.parse_args()


def load_demo_db(db_path: Path) -> None:
    """Create schema (if needed), then persist demo habits and completions."""
    schema_path = Path(__file__).resolve().parents[1] / "persistence" / "schema.sql"
    repo = SQLiteHabitRepository(db_path=db_path, schema_path=schema_path)

    try:
        demo_habits = create_demo_habits()
        populate_demo_data(demo_habits)

        for habit in demo_habits:
            repo.add_habit(habit)
            for completion in habit.completions:
                repo.add_completion(completion)
    finally:
        repo.close()


def main() -> None:
    args = parse_args()
    db_path = Path(args.db)

    if args.reset and db_path.exists():
        db_path.unlink()

    load_demo_db(db_path)
    print(f"✅ Demo database ready: {db_path.resolve()}")


if __name__ == "__main__":
    main()
