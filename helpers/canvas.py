import os
from canvasapi import Canvas
from dotenv import load_dotenv

load_dotenv()

canvas = Canvas(
    os.environ.get("CANVAS_API_BASEURL"),
    os.environ.get("CANVAS_LMS_API_TOKEN")
)