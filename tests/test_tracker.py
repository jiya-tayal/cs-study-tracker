from src.courses import Course

# Create a course object
course = Course(
    "Discrete Mathematics",
    "COMPSCI 250",
    "Professor Golin",
    "Fall 2026"
)

# Display course information
print(course.name)
print(course.course_code)
print(course.instructor)
print(course.semester)

