from datetime import date, datetime

from src.courses import Course
from src.assignments import Assignment
from src.study_sessions import StudySession
from src.storage import load_data, save_data

DATA_FILE = "data/tracker.json"


def prompt_required(label):
    """Ask for a non-empty value."""
    while True:
        value = input(label).strip()

        if value:
            return value

        print("This field is required. Please try again.")


def prompt_date(label):
    """Ask for a date in YYYY-MM-DD format."""
    while True:
        value = prompt_required(label)

        try:
            datetime.strptime(value, "%m-%d-%Y")
            return value
        except ValueError:
            print("Please use MM-DD-YYYY format.")


def prompt_positive_int(label):
    """Ask for a positive whole number."""
    while True:
        value = input(label).strip()

        try:
            number = int(value)

            if number > 0:
                return number

        except ValueError:
            pass

        print("Please enter a positive whole number.")


def choose_course(courses):
    """Let the user select a course."""

    if not courses:
        print("Add a course first.")
        return None

    for number, course in enumerate(courses, start=1):
        print(f"{number}. {course}")

    choice = input("Choose a course number: ").strip()

    if not choice.isdigit():
        print("Please enter a valid number.")
        return None

    index = int(choice) - 1

    if index < 0 or index >= len(courses):
        print("That course number does not exist.")
        return None

    return courses[index]


def display_courses(courses):
    """Display all courses."""

    print("\n===== MY COURSES =====")

    if not courses:
        print("No courses have been added yet.")
        return

    for number, course in enumerate(courses, start=1):
        print(f"{number}. {course}")


def add_course(data):
    """Create and add a new course."""

    print("\n===== ADD A COURSE =====")

    course = Course(
        prompt_required("Course name: "),
        prompt_required("Course code: "),
        prompt_required("Instructor: "),
        prompt_required("Semester: ")
    )

    if any(
        existing.course_code.lower() == course.course_code.lower()
        for existing in data["courses"]
    ):
        print("A course with that course code already exists.")
        return

    data["courses"].append(course)

    print(f"Successfully added: {course}")


def remove_course(data):
    """Remove a course without deleting its associated records."""

    print("\n===== REMOVE A COURSE =====")

    course = choose_course(data["courses"])

    if course is None:
        return

    has_assignments = any(
        item.course_code.lower() == course.course_code.lower()
        for item in data["assignments"]
    )

    has_sessions = any(
        item.course_code.lower() == course.course_code.lower()
        for item in data["study_sessions"]
    )

    if has_assignments or has_sessions:
        print("This course has assignments or study sessions attached.")
        print("Remove those records before removing the course.")
        return

    data["courses"].remove(course)

    print(f"Successfully removed: {course}")


def add_assignment(data):
    """Create and add an assignment."""

    print("\n===== ADD AN ASSIGNMENT =====")

    course = choose_course(data["courses"])

    if course is None:
        return

    title = prompt_required("Assignment title: ")
    due_date = prompt_date("Due date (MM-DD-YYYY): ")

    while True:
        priority = input(
            "Priority (low/medium/high): "
        ).strip().lower()

        if priority in {"low", "medium", "high"}:
            break

        print("Enter low, medium, or high.")

    assignment = Assignment(
        course_code=course.course_code,
        title=title,
        due_date=due_date,
        priority=priority
    )

    data["assignments"].append(assignment)

    print(f"Successfully added: {title}")


def list_assignments(data):
    """Display all assignments."""

    print("\n===== MY ASSIGNMENTS =====")

    assignments = sorted(
        data["assignments"],
        key=lambda item: item.due_date
    )

    if not assignments:
        print("No assignments have been added.")
        return

    course_names = {
        course.course_code: course.name
        for course in data["courses"]
    }

    for number, assignment in enumerate(assignments, start=1):
        status = "Complete" if assignment.completed else "Pending"

        course_name = course_names.get(
            assignment.course_code,
            assignment.course_code
        )

        print(
            f"{number}. {assignment.title} | "
            f"{course_name} | "
            f"Due: {assignment.due_date} | "
            f"Priority: {assignment.priority} | "
            f"Status: {status}"
        )


def mark_assignment_complete(data):
    """Mark a pending assignment as complete."""

    print("\n===== COMPLETE AN ASSIGNMENT =====")

    pending = [
        assignment
        for assignment in data["assignments"]
        if not assignment.completed
    ]

    if not pending:
        print("There are no pending assignments.")
        return

    for number, assignment in enumerate(pending, start=1):
        print(
            f"{number}. {assignment.title} "
            f"(Due: {assignment.due_date})"
        )

    choice = input("Choose an assignment number: ").strip()

    if not choice.isdigit():
        print("Invalid assignment number.")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(pending):
        print("That assignment does not exist.")
        return

    selected = pending[index]
    selected.completed = True

    print(f"Marked complete: {selected.title}")


def record_study_session(data):
    """Record a study session."""

    print("\n===== RECORD A STUDY SESSION =====")

    course = choose_course(data["courses"])

    if course is None:
        return

    session_date = prompt_date("Study date (MM-DD-YYYY): ")
    duration = prompt_positive_int("Duration in minutes: ")
    notes = input("Notes (optional): ").strip()

    session = StudySession(
        course_code=course.course_code,
        session_date=session_date,
        duration_minutes=duration,
        notes=notes
    )

    data["study_sessions"].append(session)

    print(f"Recorded {duration} minutes of studying.")


def display_study_sessions(data):
    """Display recorded study sessions."""

    print("\n===== STUDY HISTORY =====")

    if not data["study_sessions"]:
        print("No study sessions recorded.")
        return

    course_names = {
        course.course_code: course.name
        for course in data["courses"]
    }

    sessions = sorted(
        data["study_sessions"],
        key=lambda item: item.session_date,
        reverse=True
    )

    for session in sessions:
        course_name = course_names.get(
            session.course_code,
            session.course_code
        )

        print(
            f"{session.session_date} | "
            f"{course_name} | "
            f"{session.duration_minutes} minutes | "
            f"{session.notes}"
        )


def display_dashboard(data):
    """Display an overview of academic progress."""

    print("\n===== PROGRESS DASHBOARD =====")

    courses = data["courses"]
    assignments = data["assignments"]
    sessions = data["study_sessions"]

    completed = sum(
        assignment.completed
        for assignment in assignments
    )

    pending = len(assignments) - completed

    total_minutes = sum(
        session.duration_minutes
        for session in sessions
    )

    upcoming = sorted(
        [
            assignment
            for assignment in assignments
            if not assignment.completed
            and datetime.strptime(
                assignment.due_date, "%m-%d-%Y"
            ).date() >= date.today()
        ],
        key=lambda item: datetime.strptime(
            item.due_date, "%m-%d-%Y"
        )
    )

    print(f"Total courses: {len(courses)}")
    print(f"Total assignments: {len(assignments)}")
    print(f"Completed assignments: {completed}")
    print(f"Pending assignments: {pending}")

    print(
        f"Total study time: "
        f"{total_minutes // 60} hours "
        f"and {total_minutes % 60} minutes"
    )

    print("\nUpcoming assignments:")

    if not upcoming:
        print("No upcoming assignments.")
        return

    course_names = {
        course.course_code: course.name
        for course in courses
    }

    for assignment in upcoming[:5]:
        course_name = course_names.get(
            assignment.course_code,
            assignment.course_code
        )

        print(
            f"- {assignment.title} | "
            f"{course_name} | "
            f"{assignment.due_date} | "
            f"{assignment.priority}"
        )


def main():
    """Run the CS Study Tracker application."""

    data = load_data(DATA_FILE)

    actions = {
        "1": lambda: display_dashboard(data),
        "2": lambda: display_courses(data["courses"]),
        "3": lambda: add_course(data),
        "4": lambda: remove_course(data),
        "5": lambda: add_assignment(data),
        "6": lambda: list_assignments(data),
        "7": lambda: mark_assignment_complete(data),
        "8": lambda: record_study_session(data),
        "9": lambda: display_study_sessions(data)
    }

    while True:
        print("\n========== CS STUDY TRACKER ==========")
        print("1. View dashboard")
        print("2. View courses")
        print("3. Add a course")
        print("4. Remove a course")
        print("5. Add an assignment")
        print("6. View assignments")
        print("7. Mark an assignment complete")
        print("8. Record a study session")
        print("9. View study sessions")
        print("10. Save and exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "10":
            save_data(DATA_FILE, data)
            print("Your data has been saved. Goodbye!")
            break

        action = actions.get(choice)

        if action:
            action()
            save_data(DATA_FILE, data)
        else:
            print("Invalid choice. Please enter a number from 1 to 10.")


if __name__ == "__main__":
    main()
