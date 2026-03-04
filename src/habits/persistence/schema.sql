PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS habits (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    periodicity TEXT NOT NULL CHECK(periodicity IN ('daily', 'weekly')),
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS completions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    note TEXT,
    FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_completions_habit_id ON completions(habit_id);
CREATE INDEX IF NOT EXISTS idx_completions_timestamp ON completions(timestamp);
