# init_db.py
from app.models.base import Base
from .engine import engine


def init_db():
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)