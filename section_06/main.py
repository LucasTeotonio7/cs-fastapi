from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router


app = FastAPI(title='Course API - Security')
app.include_router(api_router, prefix=settings.API_V1_STR)



if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        "main:app", 
        host='0.0.0.0', 
        port=8010, 
        log_level='info', 
        reload=True
    )


# Debug
@app.on_event("startup")
async def startup_event():
        import logging
        import ptvsd

        logging.basicConfig(level=logging.INFO, format='\n \033[92m %(message)s \033[0m \n')
        logging.info('DEBUG SERVER STARTED AT PORT 3000')
        ptvsd.enable_attach(address=('0.0.0.0', 3010))
