from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status


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



if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app='main:app', 
        host="0.0.0.0", 
        port=8000,
        debug=True,
        reload=True
    )
