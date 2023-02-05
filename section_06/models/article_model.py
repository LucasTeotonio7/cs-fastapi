from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings


class ArticleModel(settings.DBBaseModel):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256))
    font_url = Column(String(256)),
    user_id = Column(Integer, ForeignKey('user.id'))
    created_by = relationship('UserModel', back_populates='articles', lazy='joined')
