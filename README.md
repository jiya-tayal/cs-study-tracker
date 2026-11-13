
# CS Study Tracker

A command-line Python application for organizing college courses, tracking assignment deadlines, recording study sessions, and monitoring academic progress.

## Features

- Add, view, and remove courses
- Track assignments and due dates
- Assign low, medium, and high priority levels
- Mark assignments as completed
- Record study sessions and durations
- Track total study time
- View an academic progress dashboard
- Save and load information using JSON
- Automated tests using Python's unittest framework

## Technologies

- Python
- Object-oriented programming
- JSON data storage
- unittest

## Requirements

Python 3.9 or newer.

No external packages are required.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/jiya-tayal/cs-study-tracker.git
```

Navigate into the project:

```bash
cd cs-study-tracker
```

Run the application:

```bash
python3 main.py
```

## Running Tests

Run the automated tests from the project root:

```bash
python3 -m unittest discover -s tests -v
```

## Project Structure

```text
cs-study-tracker/
├── main.py
├── src/
│   ├── courses.py
│   ├── assignments.py
│   ├── study_sessions.py
│   └── storage.py
├── data/
├── tests/
│   └── test_tracker.py
├── README.md
├── LICENSE
└── .gitignore
```

## Data Storage

The application saves course, assignment, and study session information locally in:

`data/tracker.json`

The data file is excluded from Git to keep personal academic information private.

## Future Improvements

- Graphical user interface
- Weekly study-time summaries
- Assignment filtering and search
- Study goals and progress tracking

