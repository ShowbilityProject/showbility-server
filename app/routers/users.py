from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.db.engine import get_db
from app.schemas.users import UserCreate, UserResponse\
from app.crud.users import

router = APIRouter()

@router.post("/users/", response_model=User)
async def create_user(user: User, db: AsyncSession = Depends(get_db)):
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users/", response_model=UserResponse)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_data = user.dict()
    return await create_user(db, user_data)

@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user