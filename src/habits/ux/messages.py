"""User-facing messages for the CLI.

Centralizing user-facing strings is intended to keep CLI output consistent.
"""

WELCOME_MESSAGE = """
Welcome to the Habit Tracker! 🎯
Your journey starts here. Let's build habits that last.
"""

HELP_MESSAGE = """
How to use this Habit Tracker:

1. Create a new habit:
    - 'add <habit_name> <daily|weekly>'

2. Mark a habit as completed:
    - 'complete <habit_id> [optional note]'

3. View your habit list:
    - 'list'

4. Get streak and completion statistics:
    - 'streaks'

5. Exit:
    - 'exit' or 'quit'
"""

INVALID_COMMAND_MESSAGE = "Sorry, that command was not understood. Type 'help' for usage."

EMPTY_LIST_MESSAGE = "No habits are tracked yet. Add one with 'add <habit_name> <daily|weekly>'."

STREAKS_HEADER = """
Your Streaks: 💪
-----------------
"""
