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
