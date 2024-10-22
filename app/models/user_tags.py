# app/models/user_tags.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base_class import Base

user_tags = Table(
    "user_tags",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)
