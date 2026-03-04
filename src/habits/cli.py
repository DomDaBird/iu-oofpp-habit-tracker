"""Command Line Interface (CLI) for the Habit Tracker.

This CLI is intentionally kept:
    - simple
    - readable
    - IU-conform
    - UX-polished (clear output and feedback)

Only the HabitTracker service is interacted with.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from habits.domain.enums import Periodicity
from habits.persistence.sqlite_repo import SQLiteHabitRepository
from habits.services.tracker import HabitTracker
from habits.ux.messages import (
    WELCOME_MESSAGE,
    HELP_MESSAGE,
    INVALID_COMMAND_MESSAGE,
    EMPTY_LIST_MESSAGE,
    STREAKS_HEADER,
    HABIT_NOT_FOUND_MESSAGE,
)


def _parse_periodicity(value: str) -> Periodicity:
    try:
        return Periodicity.from_user_input(value)
    except ValueError as exc:
        raise ValueError(str(exc))


def _print_habits(tracker: HabitTracker) -> None:
    habits = tracker.list_habits()
    if not habits:
        print(EMPTY_LIST_MESSAGE)
        return

    print("\nYour Habits:")
    print("-" * 40)
    for h in habits:
        print(
            f"ID: {h.id}\n"
            f"  Name       : {h.name}\n"
            f"  Periodicity: {h.periodicity.value}\n"
        )


def _print_streaks(tracker: HabitTracker) -> None:
    habits = tracker.list_habits()
    if not habits:
        print(EMPTY_LIST_MESSAGE)
        return

    print(STREAKS_HEADER)
    for h in habits:
        summary = tracker.streak_summary(h.id)
        print(
            f"{summary.habit_name} ({summary.periodicity.value})\n"
            f"  Current streak : {summary.current_streak}\n"
            f"  Longest streak : {summary.longest_streak}\n"
            f"  Total check-offs: {summary.total_completions}\n"
        )

    longest = tracker.longest_streak()
    if longest:
        print(
            f"🏆 Longest streak overall: "
            f"{longest.habit_name} ({longest.longest_streak})"
        )


def run_cli(db_path: str) -> None:
    """Start the interactive CLI loop."""
    repo = SQLiteHabitRepository(
        db_path=db_path,
        schema_path=Path(__file__).parent / "persistence" / "schema.sql",
    )
    tracker = HabitTracker(repo)

    print(WELCOME_MESSAGE)
    print("Type 'help' to see available commands.\n")

    try:
        while True:
            raw = input("> ").strip()
            if not raw:
                continue

            parts = raw.split()
            command = parts[0].lower()

            if command == "help":
                print(HELP_MESSAGE)

            elif command == "add":
                if len(parts) < 3:
                    print("Usage: add <habit_name> <daily|weekly>")
                    continue

                name = " ".join(parts[1:-1])
                periodicity = _parse_periodicity(parts[-1])

                habit = tracker.create_habit(name, periodicity)
                print(
                    "✅ Habit created:\n"
                    f"  ID: {habit.id}\n"
                    f"  Name: {habit.name}\n"
                    f"  Periodicity: {habit.periodicity.value}"
                )

            elif command == "list":
                _print_habits(tracker)

            elif command == "complete":
                if len(parts) < 2:
                    print("Usage: complete <habit_id> [optional note]")
                    continue

                habit_id = parts[1]
                note: Optional[str] = " ".join(parts[2:]) if len(parts) > 2 else None

                result = tracker.complete_habit(habit_id, note=note)

                streak = result["streak"]
                gamification = result["gamification"]

                print("✅ Habit completed!")
                print(
                    f"🔥 Current streak: {streak.current} | "
                    f"🏆 Longest streak: {streak.longest}"
                )
                print(
                    f"⭐ XP gained: {gamification.xp_gained} | "
                    f"Total XP: {gamification.new_total_xp} | "
                    f"Level: {gamification.new_level}"
                )

                for badge in gamification.badges_earned:
                    print(f"🏅 New badge earned: {badge}")

                print(f"💬 {result['sentiment_feedback']}")

            elif command == "delete":
                if len(parts) < 2:
                    print("Usage: delete <habit_id>")
                    continue

                habit_id = parts[1]

                # Friendly feedback if the habit does not exist
                if tracker.get_habit(habit_id) is None:
                    print(HABIT_NOT_FOUND_MESSAGE.format(habit_id))
                    continue

                tracker.delete_habit(habit_id)
                print(f"🗑️ Habit deleted: {habit_id}")

            elif command == "streaks":
                _print_streaks(tracker)

            elif command in {"exit", "quit"}:
                print("Goodbye! 👋 Keep building great habits.")
                break

            else:
                print(INVALID_COMMAND_MESSAGE)

    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")

    finally:
        tracker.close()


if __name__ == "__main__":
    run_cli("habits.db")
