from typing import List

from pydantic import BaseSettings, AnyHttpUrl
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    """
    Global application settings
    """

    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:admin@localhost:5432/faculty'
    DBBaseModel = declarative_base()

    JWT_SECRET: str = 'U3l-VIsX2d_-5sTSbas3rrpZF-0ftVbpVPwG-ks5eRk'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7


    class Config:
        case_sensitive = True


settings = Settings()
