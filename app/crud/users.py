# app/crud/user_crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User

async def create_user(db: AsyncSession, user_data: dict):
    user = User(**user_data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user(db: AsyncSession, user_id: int):
    return await db.get(User, user_id)