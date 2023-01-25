from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.course_model import CourseModel
from core.deps import get_session


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True

# end bypass

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CourseModel)
async def create_course(
    course: CourseModel, 
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


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[CourseModel])
async def get_courses(
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(CourseModel)
        result = await session.execute(query)
        courses: List[CourseModel] = result.scalars().all()

        return courses


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=CourseModel)
async def get_course(
    id: int, 
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == id)
        result = await session.execute(query)
        course: CourseModel = result.scalar_one_or_none()

        if course:
            return course
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Course not found'
            )


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=CourseModel)
async def update_course(
    id: int, 
    course: CourseModel, 
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == id)
        result = await session.execute(query)
        course_db: CourseModel = result.scalar_one_or_none()

        if course_db:
            course_db.title = course.title
            course_db.lessons = course.lessons
            course_db.hours = course.hours

            await session.commit()

            return course_db
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Course not found'
            )


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    id: int, 
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == id)
        result = await session.execute(query)
        course_db: CourseModel = result.scalar_one_or_none()

        if course_db:
            await session.delete(course_db)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Course not found'
            )
