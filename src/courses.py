
class Course:
    """Represent a college course."""

    def __init__(self, name, course_code, instructor, semester):
        self.name = name
        self.course_code = course_code
        self.instructor = instructor
        self.semester = semester

    def __str__(self):
        return f"{self.course_code} - {self.name} ({self.semester})"

    def to_dict(self):
        """Convert course information into a dictionary."""
        return {
            "name": self.name,
            "course_code": self.course_code,
            "instructor": self.instructor,
            "semester": self.semester
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Course object from a dictionary."""
        return cls(
            data["name"],
            data["course_code"],
            data["instructor"],
            data["semester"]
        )
