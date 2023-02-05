from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings


class UserModel(settings.DBBaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    email = Column(String(256), index=True, nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    is_superuser = Column(Boolean, default=False)
    articles = relationship(
        'ArticleModel',
        cascade='all,delete-orphan',
        back_populates='created_by',
        uselist=True,
        lazy='joined'
    )
