import tempfile
import unittest
from pathlib import Path

from src.courses import Course
from src.assignments import Assignment
from src.study_sessions import StudySession
from src.storage import load_data, save_data


class CourseTests(unittest.TestCase):

    def test_course_attributes(self):
        course = Course(
            "Discrete Mathematics",
            "COMPSCI 250",
            "Professor Golin",
            "Fall 2026"
        )

        self.assertEqual(course.course_code, "COMPSCI 250")

    def test_course_string(self):
        course = Course(
            "Discrete Mathematics",
            "COMPSCI 250",
            "Professor Golin",
            "Fall 2026"
        )

        self.assertEqual(
            str(course),
            "COMPSCI 250 - Discrete Mathematics (Fall 2026)"
        )


class AssignmentTests(unittest.TestCase):

    def test_assignment_creation(self):
        assignment = Assignment(
            "STAT 416",
            "Problem Set 1",
            "2026-11-20",
            "high"
        )

        self.assertEqual(assignment.priority, "high")
        self.assertFalse(assignment.completed)

    def test_invalid_priority(self):
        with self.assertRaises(ValueError):
            Assignment(
                "STAT 416",
                "Problem Set",
                "2026-11-20",
                "urgent"
            )


class StudySessionTests(unittest.TestCase):

    def test_study_session_creation(self):
        session = StudySession(
            "COMPSCI 250",
            "2026-11-12",
            60,
            "Induction practice"
        )

        self.assertEqual(session.duration_minutes, 60)

    def test_invalid_duration(self):
        with self.assertRaises(ValueError):
            StudySession(
                "COMPSCI 250",
                "2026-11-12",
                0
            )


class StorageTests(unittest.TestCase):

    def test_missing_file_returns_empty_data(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tracker.json"

            data = load_data(path)

            self.assertEqual(len(data["courses"]), 0)
            self.assertEqual(len(data["assignments"]), 0)
            self.assertEqual(len(data["study_sessions"]), 0)

    def test_save_and_load_data(self):
        data = {
            "courses": [
                Course(
                    "Statistics",
                    "STAT 416",
                    "Professor Westling",
                    "Fall 2026"
                )
            ],
            "assignments": [
                Assignment(
                    "STAT 416",
                    "Problem Set 1",
                    "2026-11-20",
                    "medium",
                    True
                )
            ],
            "study_sessions": [
                StudySession(
                    "STAT 416",
                    "2026-11-12",
                    45,
                    "Review"
                )
            ]
        }

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tracker.json"

            save_data(path, data)
            loaded = load_data(path)

            self.assertEqual(
                loaded["courses"][0].to_dict(),
                data["courses"][0].to_dict()
            )

            self.assertEqual(
                loaded["assignments"][0].to_dict(),
                data["assignments"][0].to_dict()
            )

            self.assertEqual(
                loaded["study_sessions"][0].to_dict(),
                data["study_sessions"][0].to_dict()
            )


if __name__ == "__main__":
    unittest.main()
