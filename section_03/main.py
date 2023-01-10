from fastapi import FastAPI
from fastapi import HTTPException, Response
from fastapi import status

from models import Course


app = FastAPI()

courses = {
    1: {
        'title': 'FastAPI - Modern and Asynchronous APIs with Python',
        'lessons': 100,
        'hours': 15
    },
    2: {
        'title': 'Programming algorithms and logic',
        'lessons': 95,
        'hours': 12
    },
}


@app.get('/courses')
async def get_courses():
    return courses

@app.get('/courses/{id}')
async def get_course(id: int):
    try:
        course = courses[id]
        return course
    except KeyError:
        raise HTTPException(
            detail='Course not found',
            status_code=status.HTTP_404_NOT_FOUND,
        )

@app.post('/courses', status_code=status.HTTP_201_CREATED)
async def create_course(course: Course):
    if course.id not in courses:
        next_id=len(courses) + 1
        courses[next_id] = course
        del course.id
        return course

@app.put('/courses/{id}')
async def update_course(id: int, course: Course):
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
async def delete_course(id: int):
    if id in courses:
        del courses[id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            detail='Course not found',
            status_code=status.HTTP_404_NOT_FOUND,
        )


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app='main:app', 
        host="0.0.0.0", 
        port=8010,
        debug=True,
        reload=True
    )
