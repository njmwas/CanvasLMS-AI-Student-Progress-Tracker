from langchain.agents import tool
from canvasapi.exceptions import ResourceDoesNotExist
from helpers import get_student_progress
from helpers.canvas import canvas
from datetime import date

def get_course_info(course):
    """Retrieving a single course and it's start and end date"""
    try:
        assignment_groups = course.get_assignment_groups()
        needed_groups = ["assignments", "required labs", "required_quizzes", "summative assessment"]
        assignment_group_ids = [g.id for g in assignment_groups if g.name.lower() in needed_groups]
        assignments = course.get_assignments(
            workflow_state="published", 
            enrollment_state="active",
            assignment_group_id=assignment_group_ids
        )

        return {"assignments":assignments, "assignment_groups":assignment_groups}
    except Exception as e:
        return f"Error occured: {e}"

# @tool
def student_progress(course, students, student_id):
    """
        Fetching a student's overall performance, content coverage progress and 
        assingment completion rate
    """
    try:
        for index, student in enumerate(students):
            if student.id == student_id:
                break

        # Get general grade perfomance
        enrollments = course.get_enrollments(user_id=student.id)
        enrollment = enrollments[0]
        grades = enrollment.grades

        output = f"""
Student{index} overall performance in {course.name} as of {date.today().strftime("%Y-%m-%d")}
Overall current grade {grades.get("current_grade", "N/A")}
Overall final grade {grades.get("final_grade", "N/A")}
"""
        # Get content coverage progress
        user_progress = get_student_progress(course.id, student.id)
        
        output += f"""
Content coverage progress:
- Completion: {user_progress["requirement_completed_count"]} (steps completed / total steps)
- Requirements count: {user_progress["requirement_count"]}
"""

        # Assignment submission rate
        course_info = get_course_info(course)
        assignments = course_info["assignments"]
        
        # unsubmitted_assignments = unsubmitted
        assignment_ids = [a.id for a in assignments]
        submissions = course.get_multiple_submissions(
            student_ids=[student.id], 
            assignment_ids=assignment_ids,
            workflow="submitted",
            per_page=100
        )

        total_assignments=len(assignment_ids)
        submitted_assignments = 0
        for submission in submissions:
            if submission.assignment_id in assignment_ids:
                submitted_assignments += 1

        output += f"""
Assignment submission rate:
Required assignments: {total_assignments}
Submitted assignments: {submitted_assignments}
"""

        return output

    except ResourceDoesNotExist as e:
        return f"Missing resource {e}"
    except Exception as e:
        return f"Error occured {e}"

