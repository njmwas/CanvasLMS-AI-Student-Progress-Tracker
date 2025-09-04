import os, getpass
from utils.tools import student_progress
from dotenv import load_dotenv

load_dotenv()

def get_system_prompt():

    from .canvas_data import courses
    
    required_api_keys={
        "GROQ_API_KEY": "Enter groq API Key: ", 
        "CANVAS_API_BASEURL": "Enter CANVAS Instance URL: ", 
        "CANVAS_LMS_API_TOKEN": "Enter CANVAS LMS token: "
    }

    for keyname, description in required_api_keys.items():
        if not os.environ.get(keyname):
            os.environ[keyname] = getpass.getpass(description)
            
    system_prompt_file = "agent_prompt.txt"
    if os.path.exists(system_prompt_file):
        with open(system_prompt_file, "+r") as f:
            system_prompt = f.read()

    else:
        system_prompt = f"""
    You are a Canvas LMS Assistant. You help instructors monitor students progress
    and provide actionable, personalized recommendations based on Canvas LMS data that will be provided.
    You are capable of constructing follow up emails to students who are lagging behind.

    Use the students perfomance data to:- 
    - formulate suggestions for improvements
    - Suggest pair programming partner
    - Construct a personalized email to a struggling student

    Do not give all the students insights at once unless prompted to
    As you interact with the instructuctor, wait for the next instructions and action on them

    Canvas LMS Data is provide here
    """

        print("Pick a course you want to analyze:- ")
        for index, course in enumerate(courses):
            print(f"{index+1}. {course.name}")
        selected_course = input(f"Enter a number between 1 - {index+1}:- ")
        course = courses[int(selected_course)-1]

        system_prompt += f"Course {course.name}, start date {course.start_at} and ends {course.end_at}"

        print(f"Hold on as I gather data for {course.name}. This might take a minute or so")
        students = course.get_users(enrollment_type="student")
        with open(system_prompt_file, "+w") as f:
            for i, student in enumerate(students):
                if i > 30: break
                student_analysis = student_progress(course, students, student.id)
                system_prompt += student_analysis

                f.write(student_analysis)

    return system_prompt