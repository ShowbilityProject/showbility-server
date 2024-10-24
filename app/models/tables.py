# app/models/tables.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models.base import Base

user_tags = Table(
    "user_tags", Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)
