from fastapi import FastAPI


app = FastAPI()


@app.get('/')
async def root():
    return {"message": "FastAPI works!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app='main:app', 
        host="0.0.0.0", 
        log_level="info", 
        reload=True
    )
