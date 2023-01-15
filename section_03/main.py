from typing import Any, Dict, List, Optional
from fastapi import FastAPI
from fastapi import HTTPException, Response
from fastapi import status
from fastapi import Path, Query, Header, Depends

from time import sleep

from models import Course, courses

from docs.course import *
from docs.calculator import *


def fake_db():
    try:
        print('opening database connection')
        sleep(1)
    finally:
        print('closing database connection')
        sleep(1)


app = FastAPI(
    title='Geek university courses api',
    version="0.0.1",
    description="An API for studying fastAPI"
)


@app.get('/courses', **get_course_doc)
async def get_courses(db: Any = Depends(fake_db)):
    return courses

@app.get('/courses/{id}', **get_course_id_doc)
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

@app.post('/courses', status_code=status.HTTP_201_CREATED)
async def create_course(course: Course, db: Any = Depends(fake_db)):
    if course.id not in courses:
        next_id=len(courses) + 1
        courses[next_id] = course
        del course.id
        return course

@app.put('/courses/{id}')
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


@app.delete('/courses/{id}')
async def delete_course(id: int, db: Any = Depends(fake_db)):
    if id in courses:
        del courses[id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            detail='Course not found',
            status_code=status.HTTP_404_NOT_FOUND,
        )


@app.get('/calculator', **get_calculator_doc)
async def calculate(
    a: int = Query(default=0, gt=5), 
    b: int = Query(default=0, gt=10),
    x_geek: str = Header(default=None),
    c: Optional[int]=0):

    print(f'X_GEEK {x_geek}')

    result = a + b + c
    return {"result": result}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app='main:app', 
        host="0.0.0.0", 
        port=8010,
        debug=True,
        reload=True
    )
