from app.models.base import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), default='')
    phone_number = Column(String(13), unique=True, nullable=True)
    username = Column(String(50), unique=True)