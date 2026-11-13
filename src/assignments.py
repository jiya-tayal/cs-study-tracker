
class Assignment:
    """Represent an assignment belonging to a course."""

    VALID_PRIORITIES = {"low", "medium", "high"}

    def __init__(
        self,
        course_code,
        title,
        due_date,
        priority="medium",
        completed=False
    ):
        if priority not in self.VALID_PRIORITIES:
            raise ValueError("Priority must be low, medium, or high.")

        self.course_code = course_code
        self.title = title
        self.due_date = due_date
        self.priority = priority
        self.completed = bool(completed)

    def to_dict(self):
        """Convert assignment information into a dictionary."""
        return {
            "course_code": self.course_code,
            "title": self.title,
            "due_date": self.due_date,
            "priority": self.priority,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Assignment object from a dictionary."""
        return cls(
            course_code=data["course_code"],
            title=data["title"],
            due_date=data["due_date"],
            priority=data.get("priority", "medium"),
            completed=data.get("completed", False)
        )
