from habits.analytics.analytics import habit_with_longest_streak
from habits.domain.habit import Habit
from habits.domain.enums import Periodicity
from habits.domain.completion import Completion
from datetime import datetime, timedelta


def test_habit_with_longest_streak():
    h1 = Habit("Habit 1", Periodicity.DAILY)
    h2 = Habit("Habit 2", Periodicity.DAILY)

    now = datetime.utcnow()

    # h1: 2-day streak
    for i in range(2):
        h1.add_completion(
            Completion(habit_id=h1.id, timestamp=now - timedelta(days=i))
        )

    # h2: 4-day streak
    for i in range(4):
        h2.add_completion(
            Completion(habit_id=h2.id, timestamp=now - timedelta(days=i))
        )

    result = habit_with_longest_streak([h1, h2])

    assert result is not None
    assert result.habit_name == "Habit 2"
    assert result.longest_streak == 4
