from pytz import timezone


from typing import Optional, List
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer


from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.user_model import UserModel
from core.configs import settings
from core.security import check_password

from pydantic import EmailStr


oauth2schema = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_V1_STR}/users/login'
)

async def authenticate(
    email: EmailStr,
    password: str,
    db: AsyncSession
) -> Optional[UserModel]:

    async with db as session:
        query = select(UserModel).filter(
            UserModel.email == email,
        )
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            return None

        if not check_password(password, user.password):
            return None

        return user


def create_token(
    type: str,
    expiry_time: timedelta,
    sub: str
) -> str:

    payload = {}
    tz = timezone('America/Sao_Paulo')
    expiry = datetime.now(tz) + expiry_time

    payload["type"] = type
    payload["exp"] = expiry
    payload["iat"] = datetime.now(tz)
    payload["sub"] = str(sub)

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.ALGORITHM
    )

def create_access_token(sub: str) -> str:

    return create_token(
        type='access_token',
        expiry_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )
