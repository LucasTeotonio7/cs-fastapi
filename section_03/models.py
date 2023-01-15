from pydantic import BaseModel
from typing import Optional


class Course(BaseModel):
    id: Optional[int] = None
    title: str
    lessons: int
    hours: int


courses = [
    Course(id=1, title='FastAPI - Modern and Asynchronous APIs with Python', lessons=100, hours=15),
    Course(id=2, title='Programming algorithms and logic', lessons=95, hours=12)
]