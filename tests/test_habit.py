from habits.domain.habit import Habit
from habits.domain.enums import Periodicity
from habits.domain.completion import Completion


def test_create_habit():
    habit = Habit(name="Test Habit", periodicity=Periodicity.DAILY)

    assert habit.name == "Test Habit"
    assert habit.periodicity == Periodicity.DAILY
    assert habit.total_completions() == 0


def test_add_completion():
    habit = Habit(name="Test Habit", periodicity=Periodicity.DAILY)
    completion = Completion.now(habit_id=habit.id)

    habit.add_completion(completion)

    assert habit.total_completions() == 1
    assert habit.completions[0].habit_id == habit.id
