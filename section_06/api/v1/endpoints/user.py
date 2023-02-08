from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import UserModel
from schemas.user_schema import UserSchemaBase, UserSchemaCreate, UserSchemaUpdate, UserSchemaArticles
from core.deps import get_session, get_current_user
from core.security import create_password_hash
from core.auth import authenticate, create_access_token


router = APIRouter()


@router.get('/logged', response_model=UserSchemaBase)
def get_logged(user_logged: UserModel = Depends(get_current_user)):
    return user_logged

@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def create_user(
    user: UserSchemaCreate, 
    db: AsyncSession = Depends(get_session)
):
    new_user = UserModel(
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        password = create_password_hash(user.password),
        is_superuser = user.is_superuser
    )

    async with db as session:
        session.add(new_user)
        await session.commit()

        return new_user

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserSchemaBase])
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserSchemaBase] = result.scalars().unique().all()

        return users

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserSchemaArticles)
async def get_user(
    id: int, 
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == id)
        result = await session.execute(query)
        user: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user:
            return user

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='User not found'
        )

@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=UserSchemaBase)
async def update_user(
    id: int,
    user: UserSchemaUpdate,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == id)
        result = await session.execute(query)
        user_db: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user_db:

            user_db.first_name = user.first_name or user_db.first_name
            user_db.last_name = user.last_name or user_db.last_name
            user_db.email = user.email or user_db.email
            user_db.is_superuser = user.is_superuser or user_db.is_superuser
            user_db.password = create_password_hash(user.password) or user_db.password

            await session.commit()

            return user_db

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='User not found'
        )

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: int, 
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == id)
        result = await session.execute(query)
        user_db: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user_db:
            await session.delete(user_db)
            session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='User not found'
        )

@router.post('/login')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
):
    user = authenticate(email=form_data.username, password=form_data.password, db=db)

    if not user:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Incorrect authentication data'
        )

    return JSONResponse(
        {
            "access_token": create_access_token(sub=user.id),
            "token_type": "bearer",
        },
        status_code=status.HTTP_200_OK,
    )
