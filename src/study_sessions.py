
class StudySession:
    """Represent a study session for a course."""

    def __init__(
        self,
        course_code,
        session_date,
        duration_minutes,
        notes=""
    ):
        if not isinstance(duration_minutes, int) or duration_minutes <= 0:
            raise ValueError("Study duration must be a positive whole number.")

        self.course_code = course_code
        self.session_date = session_date
        self.duration_minutes = duration_minutes
        self.notes = notes

    def to_dict(self):
        """Convert study session information into a dictionary."""
        return {
            "course_code": self.course_code,
            "session_date": self.session_date,
            "duration_minutes": self.duration_minutes,
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, data):
        """Create a StudySession object from a dictionary."""
        return cls(
            course_code=data["course_code"],
            session_date=data["session_date"],
            duration_minutes=data["duration_minutes"],
            notes=data.get("notes", "")
        )

