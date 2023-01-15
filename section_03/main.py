from fastapi import FastAPI

from routers import course_router, calculator_router


app = FastAPI(
    title='Geek university courses api',
    version="0.0.1",
    description="An API for studying fastAPI"
)

app.include_router(course_router.router)
app.include_router(calculator_router.router)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app='main:app', 
        host="0.0.0.0", 
        port=8010,
        debug=True,
        reload=True
    )
