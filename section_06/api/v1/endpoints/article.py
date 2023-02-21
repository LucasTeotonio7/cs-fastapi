from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from models import ArticleModel, UserModel
from schemas.article_schema import ArticleSchema
from core.deps import get_session, get_current_user


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ArticleSchema)
async def create_article(
    article: ArticleSchema,
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    new_article = ArticleModel(
        title=article.title,
        description=article.description,
        font_url=article.font_url,
        user_id=user.id
    )
    db.add(new_article)
    await db.commit()

    return new_article


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ArticleSchema])
async def get_articles(
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(ArticleModel)
        result = await session.execute(query)
        articles: List[ArticleModel] = result.scalars().unique().all()

        return articles


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ArticleSchema)
async def get_article(
    id: int, 
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == id)
        result = await session.execute(query)
        article: ArticleModel = result.unique().scalar_one_or_none()

        if article:
            return article
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Article not found'
            )


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ArticleSchema)
async def update_article(
    id: int,
    article: ArticleSchema,
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == id)
        result = await session.execute(query)
        article_db: ArticleModel = result.unique().scalar_one_or_none()

        if article_db:
            article_db.title = article.title or article_db.title
            article_db.description = article.description or article_db.description
            article_db.font_url = article.font_url or article_db.font_url

            if user.id != article_db.user_id:
                article_db.user = article.user_id

            await session.commit()
            return article_db

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Article not found'
            )


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    id: int,
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = (select(ArticleModel)
            .filter(ArticleModel.id == id)
            .filter(ArticleModel.user_id == user.id)
        )
        result = await session.execute(query)
        article_db: ArticleModel = result.unique().scalar_one_or_none()

        if article_db:
            await session.delete(article_db)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)

        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail='Article not found'
            )
