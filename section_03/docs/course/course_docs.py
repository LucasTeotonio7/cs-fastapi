from typing import List
from models import Course


get_course_doc = {
    "description":"returns all courses or an empty list", 
    "summary":"returns all courses",
    "response_model":List[Course],
    "response_description":"courses successfully found"
}


get_course_id_doc = {
    "description":"returns a courses by id", 
    "response_model": Course,
    "response_description":"course successfully found"
}
