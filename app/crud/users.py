# app/crud/user_crud.py
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.models.users import User
#
# async def create_user(db: AsyncSession, user_data: dict):
#     user = User(**user_data)
#     db.add(user)
#     await db.commit()
#     await db.refresh(user)
#     return user
#
# async def get_user(db: AsyncSession, user_id: int):
#     return await db.get(User, user_id)


# crud/users.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.users import ExtendUser
from app.schemas.users import UserCreate
from app.core.security import get_password_hash, create_access_token
from fastapi import HTTPException

def create_user(session: Session, user_create: UserCreate):
    try:
        hashed_password = get_password_hash(user_create.password)
        db_user = ExtendUser(username=user_create.username,
                       nickname=user_create.nickname,
                       hashed_password=hashed_password,
                       agreeRule=user_create.agreeRule,
                       agreeMarketing=user_create.agreeMarketing,
                       name=user_create.name,
                       phone_number=user_create.phone_number)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        token = create_access_token(user_id=db_user.id)

        return {"token": token}
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="User creation failed: Username or email already exists")