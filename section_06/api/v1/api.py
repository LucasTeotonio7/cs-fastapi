from fastapi import APIRouter

from api.v1.endpoints import article, user


api_router = APIRouter()


api_router.include_router(article.router, prefix='articles', tags=['articles'])
api_router.include_router(article.user, prefix='users', tags=['users'])
