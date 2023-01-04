from pydantic import BaseModel
from typing import Optional


class Course(BaseModel):
    id: Optional[int] = None
    title: str
    lessons: int
    hours: int
