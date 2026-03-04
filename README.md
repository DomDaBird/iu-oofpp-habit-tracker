# Habit Tracking Application

Object-Oriented and Functional Programming (Python)

---

## Project Context

This project was developed as part of the IU course  
*Object-Oriented and Functional Programming (OOFPP).*

The submission includes:

- Phase 1 – Concept Document
- Phase 2 – Presentation & Implementation Results
- Phase 3 – Final Implementation

This repository contains the complete source code, documentation, and tests required to run and evaluate the application locally.

---

## Overview

The application is a modular habit tracking backend implemented in Python.

Core features:

- Create daily and weekly habits
- Record habit completions
- Calculate streaks using functional programming principles
- Persist data in a SQLite database
- Provide gamified feedback (XP, levels, badges)
- Generate sentiment-based feedback messages

The system follows a layered architecture to ensure maintainability, separation of concerns, and testability.

---

## Architecture

The system is structured into the following layers:

- CLI Layer – User interaction
- Service Layer (HabitTracker) – Application API boundary
- Domain Layer – Core OOP logic (Habit, Completion)
- Analytics Layer – Pure functional streak calculation
- Persistence Layer – SQLite repository
- UX Layer – Gamification and sentiment feedback

Dependencies are strictly one-directional via the service layer.

---

## Folder Structure

The project structure inside this repository is organised as follows:

- docs/ – Phase 1 and Phase 2 submission documents
- src/ – Application source code
- tests/ – Unit tests (pytest)
- pyproject.toml – Package configuration
- pytest.ini – Test configuration
- requirements.txt – Minimal dependency list (pytest for testing)

Note: The file `habits.db` is generated locally after running

python -m habits.fixtures.load_demo_db --reset

and is not part of the repository.

---

## Requirements

- Python 3.10 or higher
- pip (Python package manager)

---

## Installation & Setup

### 1 Clone the repository

Clone the repository or download it as a ZIP file.  
Open a terminal in the project root directory.

### 2 Create a virtual environment

```
python -m venv .venv
```

Activate:

Windows PowerShell

```
.\.venv\Scripts\Activate.ps1
```

Windows cmd

```
.\.venv\Scripts\activate.bat
```

macOS / Linux

```
source .venv/bin/activate
```

### 3 Install the project

```
pip install -e .
```

Run application:

```
python -m habits.cli
```

---

## Demo Database (4 Weeks Test Data)

The project includes predefined habits and example tracking data covering **4 weeks**.

Generate demo data:

```
python -m habits.fixtures.load_demo_db --reset
```

This will create:

habits.db

in the project root directory.

---

## Running the Application (CLI)

Start the CLI interface:

```
python -m habits.cli
```

Available commands:

```
add <name> <daily|weekly>
list [daily|weekly]
complete <habit_id> [note]
delete <habit_id>
streaks
exit | quit
```

Example:

```
add Read daily
list
complete <habit_id_from_list> "Felt productive today"
streaks
```

---

## Running Tests

Unit tests are implemented using **pytest**.

Run all tests with:

```
python -m pytest
```

Test coverage includes:

- Domain logic validation
- Functional streak calculations
- SQLite persistence layer
- CLI import smoke test

---

## Evaluation Guide

For quick evaluation:

1 Install the project

pip install -e .

2 Generate demo database

python -m habits.fixtures.load_demo_db --reset

3 Start CLI

python -m habits.cli

4 Run analytics

streaks

5 Run tests

python -m pytest

---

## Design Principles

This project demonstrates the combination of **Object-Oriented Programming** and **Functional Programming**.

Object-Oriented Programming:

- Habit domain modeling
- Encapsulation of behavior in classes
- Clear separation of responsibilities

Functional Programming:

- Deterministic streak calculations
- Pure analytics functions without side effects

Additional principles:

- Repository Pattern for persistence
- Layered Architecture
- Automated testing with pytest

---

## Author

Dominik Vogel  
IU Internationale Hochschule  
Course: Object-Oriented and Functional Programming (OOFPP)
