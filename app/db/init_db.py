# init_db.py
from app.models.base import Base
from .engine import engine

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)