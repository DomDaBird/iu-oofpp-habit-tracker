from datetime import datetime, timedelta

from habits.analytics.streaks import streaks_for_timestamps
from habits.domain.enums import Periodicity


def test_daily_streak_simple():
    now = datetime.utcnow()
    timestamps = [
        now - timedelta(days=2),
        now - timedelta(days=1),
        now,
    ]

    result = streaks_for_timestamps(timestamps, Periodicity.DAILY)

    assert result.current == 3
    assert result.longest == 3


def test_weekly_streak_simple():
    now = datetime.utcnow()
    timestamps = [
        now - timedelta(weeks=2),
        now - timedelta(weeks=1),
        now,
    ]

    result = streaks_for_timestamps(timestamps, Periodicity.WEEKLY)

    assert result.current == 3
    assert result.longest == 3
