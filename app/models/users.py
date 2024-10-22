from app.models.base import Base
from sqlalchemy import Column, Integer, String

from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func
from app.models.base import Base
import os
from datetime import datetime
from PIL import Image as PImage, ImageOps
from io import BytesIO
import enum


class LoginType(enum.Enum):
    EMAIL = 'EM'
    KAKAO = 'KA'
    SUPER = 'SP'
    APPLE = 'AP'

# user_tags = Table(
#     'user_tags', Base.metadata,
#     Column('user_id', ForeignKey('users.id'), primary_key=True),
#     Column('tag_id', ForeignKey('tags.id'), primary_key=True)
# )


class ExtendUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), default='')
    phone_number = Column(String(13), unique=True, nullable=True)
    username = Column(String(50), unique=True)
    url = Column(String(500), nullable=True, default='')
    description = Column(String(1000), nullable=True, default='')
    nickname = Column(String(20), unique=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    agree_rule = Column(Boolean, default=True)
    agree_marketing = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    login_type = Column(Enum(LoginType), default=LoginType.EMAIL)

    profile_image = Column(String, nullable=True)
    small_image = Column(String, nullable=True)

    codes = relationship("VerificationCode", back_populates="user", cascade="all, delete")
    # tags = relationship('Tag', secondary='user_tags', back_populates='users')
    # followings = relationship('Following', foreign_keys='Following.following_user_id', back_populates="following_user")
    # followers = relationship('Following', foreign_keys='Following.followed_user_id', back_populates="followed_user")

    def __repr__(self):
        return self.username

class WithdrawUser(Base):
    __tablename__ = 'withdraw_users'

    id = Column(Integer, primary_key=True, index=True)
    old_id = Column(Integer, nullable=False)
    username = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

