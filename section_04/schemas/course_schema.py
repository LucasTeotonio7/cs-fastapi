from typing import Optional

from pydantic import BaseModel as SCBaseModel


class CourseSchema(SCBaseModel):
    id: Optional[int]
    title: str
    lessons: int
    hours: int

    class Config:
        orm_mode = True
