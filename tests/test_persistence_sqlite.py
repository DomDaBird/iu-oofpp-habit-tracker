from pathlib import Path

from habits.domain.enums import Periodicity
from habits.persistence.sqlite_repo import SQLiteHabitRepository
from habits.domain.habit import Habit
from habits.domain.completion import Completion


def test_sqlite_repository(tmp_path: Path):
    # 1) Create a temporary DB file path
    db_path = tmp_path / "test.db"

    # 2) Point to the schema file in your project
    schema_path = Path("src/habits/persistence/schema.sql")

    # 3) Create repository (applies schema)
    repo = SQLiteHabitRepository(db_path, schema_path)

    # 4) Add a habit
    habit = Habit("Test Habit", Periodicity.DAILY)
    repo.add_habit(habit)

    # 5) Add a completion
    completion = Completion.now(habit.id)
    repo.add_completion(completion)

    # 6) Load habit (should include completions)
    loaded = repo.get_habit(habit.id)

    assert loaded is not None
    assert loaded.name == "Test Habit"
    assert loaded.periodicity == Periodicity.DAILY
    assert loaded.total_completions() == 1

    repo.close()
