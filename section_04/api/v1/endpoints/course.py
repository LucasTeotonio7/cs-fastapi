from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.course_model import CourseModel
from schemas.course_schema import CourseSchema
from core.deps import get_session


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CourseSchema)
async def create_course(
    course: CourseSchema, 
    db: AsyncSession = Depends(get_session)
):
    new_course = CourseModel(
        title=course.title,
        lessons=course.lessons,
        hours=course.hours
    )
    db.add(new_course)
    await db.commit()

    return new_course


@router.get('/', status_code=status.HTTP_200_OK, response_model=CourseSchema)
async def get_courses(
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(CourseModel)
        result = await session.execute(query)
        courses: List[CourseModel] = result.scarlars().all()

        return courses
