from habits.fixtures.seed_data import create_demo_habits, populate_demo_data
from habits.domain.enums import Periodicity


def test_demo_habits_exist_and_periodicity():
    """
    Requirement:
    - 5 predefined habits
    - at least one daily and one weekly habit
    """
    habits = create_demo_habits()

    assert len(habits) == 5

    periodicities = {h.periodicity for h in habits}

    assert Periodicity.DAILY in periodicities
    assert Periodicity.WEEKLY in periodicities


def test_demo_data_generates_completions():
    """
    Requirement:
    demo habits must include example tracking data.
    """
    habits = create_demo_habits()
    populate_demo_data(habits)

    completion_counts = [len(h.completions) for h in habits]

    # ensure every habit has completion entries
    assert all(count > 0 for count in completion_counts)


def test_demo_data_spans_about_4_weeks():
    """
    Requirement:
    example tracking data covering ~4 weeks.
    """
    habits = create_demo_habits()
    populate_demo_data(habits)

    timestamps = []

    for habit in habits:
        for completion in habit.completions:
            timestamps.append(completion.timestamp)

    timestamps.sort()

    span_days = (timestamps[-1].date() - timestamps[0].date()).days

    # 4 weeks = 28 days (allowing minimal tolerance)
    assert span_days >= 27