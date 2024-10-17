from pydantic import BaseModel, EmailStr, Field, constr
from datetime import datetime
from typing import Optional, List, Any
from enum import Enum
import re
from fastapi import HTTPException

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    agreeRule: bool
    agreeMarketing: bool
    name: Optional[str]
    phone_number: Optional[str]

class UserSignupResponse(BaseModel):
    token: str