from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    phone_number: str
    username: str

class UserResponse(BaseModel):
    id: int
    name: str
    phone_number: str
    username: str

    class Config:
        orm_mode = True  # ORM 모델을 Pydantic 모델로 변환할 수 있게 설정