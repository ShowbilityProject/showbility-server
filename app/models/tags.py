# app/models/tags.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.tables import user_tags


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True)
    section = Column(String(20), nullable=True)

    users = relationship("ExtendUser", secondary=user_tags, back_populates="tags")