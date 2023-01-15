from fastapi import APIRouter
from typing import Any
from fastapi import HTTPException, Response
from fastapi import status
from fastapi import Path, Depends

from time import sleep

from models import Course, courses

from docs.course import *


def fake_db():
    try:
        print('opening database connection')
        sleep(1)
    finally:
        print('closing database connection')
        sleep(1)


router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.get('/', **get_course_doc)
async def get_courses(db: Any = Depends(fake_db)):
    return courses

@router.get('/{id}', **get_course_id_doc)
async def get_course(
    id: int = Path(default=None, title='course id', description='only whole numbers.', gt=0, lt=3),
    db: Any = Depends(fake_db)
):
    try:
        course = courses[id]
        return course
    except KeyError:
        raise HTTPException(
            detail='Course not found',
            status_code=status.HTTP_404_NOT_FOUND,
        )

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_course(course: Course, db: Any = Depends(fake_db)):
    if course.id not in courses:
        next_id=len(courses) + 1
        course.id = next_id
        courses.append(course)
        return course

@router.put('/{id}')
async def update_course(id: int, course: Course, db: Any = Depends(fake_db)):
    if id in courses:
        course = courses[id] = course
        del course.id
        return course
    else:
        raise HTTPException(
            detail='Course not found',
            status_code=status.HTTP_404_NOT_FOUND,
        )


@router.delete('/{id}')
async def delete_course(id: int, db: Any = Depends(fake_db)):
    if id in courses:
        del courses[id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            detail='Course not found',
            status_code=status.HTTP_404_NOT_FOUND,
        )
