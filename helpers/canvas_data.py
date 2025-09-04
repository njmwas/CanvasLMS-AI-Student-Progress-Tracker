from .canvas import canvas
import os, requests

courses = canvas.get_courses(per_page=100)

def get_student_progress(course_id, student_id):
    
    headers = {
        'Authorization': f'Bearer {os.environ.get("CANVAS_LMS_API_TOKEN")}',
        'Content-Type': 'application/json'
    }
    
    url = f"{os.environ.get("CANVAS_API_BASEURL")}/api/v1/courses/{course_id}/users/{student_id}/progress"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None