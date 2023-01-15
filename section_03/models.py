from pydantic import BaseModel, validator
from typing import Optional


class Course(BaseModel):
    id: Optional[int] = None
    title: str
    lessons: int
    hours: int

    @validator('title')
    def validate_title(cls, value: str):
        words = value.split(' ')
        if len(words) < 3:
            raise ValueError('the title must have at least 3 words')
        if value.islower():
            raise ValueError('the title must have the first letter capitalized')
            
        return value



courses = [
    Course(id=1, title='FastAPI - Modern and Asynchronous APIs with Python', lessons=100, hours=15),
    Course(id=2, title='Programming algorithms and logic', lessons=95, hours=12)
]