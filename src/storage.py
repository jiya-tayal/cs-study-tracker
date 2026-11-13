
import json
from pathlib import Path

from src.courses import Course
from src.assignments import Assignment
from src.study_sessions import StudySession


def load_data(file_path):
    """Load tracker information from a JSON file."""

    path = Path(file_path)

    if not path.exists():
        return {
            "courses": [],
            "assignments": [],
            "study_sessions": []
        }

    with path.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)

    return {
        "courses": [
            Course.from_dict(item)
            for item in raw_data.get("courses", [])
        ],
        "assignments": [
            Assignment.from_dict(item)
            for item in raw_data.get("assignments", [])
        ],
        "study_sessions": [
            StudySession.from_dict(item)
            for item in raw_data.get("study_sessions", [])
        ]
    }


def save_data(file_path, data):
    """Save tracker information to a JSON file."""

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    serializable_data = {
        "courses": [
            course.to_dict()
            for course in data["courses"]
        ],
        "assignments": [
            assignment.to_dict()
            for assignment in data["assignments"]
        ],
        "study_sessions": [
            session.to_dict()
            for session in data["study_sessions"]
        ]
    }

    with path.open("w", encoding="utf-8") as file:
        json.dump(serializable_data, file, indent=4)
