from fastapi import FastAPI


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



if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app='main:app', 
        host="0.0.0.0", 
        port=8000,
        debug=True,
        reload=True
    )
