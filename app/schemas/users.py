# app/schemas/users.py
from pydantic import BaseModel, EmailStr, Field, constr
from datetime import datetime
from typing import Optional, List, Any
from enum import Enum
import re
from fastapi import HTTPException

class LoginType(str, Enum):
    EMAIL = 'EM'
    KAKAO = 'KA'
    SUPER = 'SP'
    APPLE = 'AP'

class UserBase(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    username: str
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_image: Optional[str] = None
    agree_rule: bool = True
    agree_marketing: bool = False
    tags: Optional[List[TagResponse]]

class UserCreate(UserBase):
    password: str

class UserSignupResponse(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

class UserResponse(UserBase):
    id: int
    small_image: Optional[str]
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None
    phone_number: Optional[constr(max_length=15)] = None
    name: Optional[str] = None
    description: Optional[str] = None
    profile_image: Optional[str] = None
    small_image: Optional[str] = None
    tags: Optional[List[str]] = None

class WithdrawUserResponse(BaseModel):
    id: int
    old_id: int
    username: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
