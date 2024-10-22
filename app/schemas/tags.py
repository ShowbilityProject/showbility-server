# app/schemas/tags.py
from pydantic import BaseModel

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: int