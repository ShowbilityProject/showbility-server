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

user_tags = Table(
    'user_tags', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)


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

    profile_image = Column(String, nullable=True) # URL
    small_image = Column(String, nullable=True) # 썸네일 URL
    content_images = relationship("Image", back_populates="owner")

    tags = relationship('Tag', secondary='user_tags', back_populates='users')
    followings = relationship('Following', foreign_keys='Following.following_user_id', back_populates="following_user")
    followers = relationship('Following', foreign_keys='Following.followed_user_id', back_populates="followed_user")


    def get_upload_path(self, image_size, filename):
        group_name = self.username  # username이 Pydantic 모델에서 유효한 값이어야 함 # 무슨의미인지?
        base_path = os.getenv("PERSONAL_IMAGE_PATH")  # config에 설정 필요
        path = os.path.join(base_path, group_name, image_size, filename)
        return path

    def get_original_upload_path(self, filename):
        return self.get_upload_path('original', filename)

    def get_small_upload_path(self, filename):
        return self.get_upload_path('small', filename)

    def make_thumbnail(self, image_url, size=(350, 350)):
        nimage = PImage.open(image_url)
        new_image = ImageOps.exif_transpose(nimage)
        new_image.thumbnail(size, PImage.ANTIALIAS)
        thumb_io = BytesIO()
        if new_image.mode in ("RGBA", "P"):
            new_image = new_image.convert("RGB")
        new_image.save(thumb_io, 'JPEG')
        return thumb_io.getvalue()  # JPEG로 변환된 이미지 데이터 반환

    def save(self, session: Session, *args, **kwargs):
        if self.profile_image:
            self.small_image = self.make_thumbnail(self.profile_image)
        session.add(self)
        session.commit()

    def __repr__(self):
        return self.username
