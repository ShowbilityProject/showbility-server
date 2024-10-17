# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from app.models.users import User
# from app.db.engine import get_db
# from app.schemas.users import UserCreate, UserResponse
# from app.crud.users import create_user, get_user
#
# router = APIRouter()
#
# @router.post("/users/", response_model=UserResponse)
# async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
#     user_data = user.dict()
#     return await create_user(db, user_data)
#
# @router.get("/users/{user_id}", response_model=UserResponse)
# async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
#     user = await get_user(db, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# 동기 코드
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import Any
#
# from app.crud.users import create_user, get_user
# from app.schemas.users import UserCreate, UserResponse
# from app.db.engine import get_db
#
# router = APIRouter()
#
#
# @router.get(
#     "/{user_id}",
#     response_model=UserResponse
# )
# def read_user(user_id: int, db: Session = Depends(get_db)) -> Any:
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
#
#
# @router.post(
#     "/",
#     response_model=UserResponse
# )
# def create_new_user(user_in: UserCreate, db: Session = Depends(get_db)) -> Any:
#     user = create_user(db=db, user_create=user_in)
#     return user

## 이전 코드
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from app.crud.users import create_user
from app.schemas.users import UserCreate, UserResponse
from app.db.engine import get_db
#
# router = APIRouter()


# @router.get(
#     "/{user_id}",
#     response_model=UserResponse
# )
# async def read_user(user_id: int, db: AsyncSession = Depends(get_db)) -> Any:
#     result = await db.execute(
#         select(User).filter(User.id == user_id)
#     )
#     user = result.scalar_one_or_none()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# @router.post(
#     "/users",
#     response_model=UserResponse
# )
# def create_new_user(user_in: UserCreate, session: AsyncSession = Depends(get_db)) -> Any:
#     user = create_user(session=session, user_create=user_in)
#     return user

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.users import create_user
from app.schemas.users import UserCreate, UserSignupResponse
from app.api.deps import SessionDep, CurrentUser
from typing import Any

router = APIRouter()

@router.post("/users", response_model=UserSignupResponse)
def create_new_user(
    user_in: UserCreate,
    session: SessionDep
) -> Any:
    user = create_user(session=session, user_create=user_in)
    return user