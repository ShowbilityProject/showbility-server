# app/routers/users.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form, status
from typing import Any, Optional
from app.crud.users import create_user, remove_user_from_db, get_user, authenticate_user, update_user
from app.schemas.users import UserSignupResponse, UserCreate, UserResponse, TokenResponse, UserUpdate
from app.api.deps import SessionDep, CurrentUser, is_self
from app.utils.image_handler import get_upload_path, save_image, make_thumbnail, delete_user_folder
from app.models.users import ExtendUser
from app.core.security import create_access_token

router = APIRouter()

@router.post("/users", response_model=UserSignupResponse)
def create_new_user(
    session: SessionDep,
    username: str = Form(...),
    password: str = Form(...),
    nickname: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    agree_rule: bool = Form(True),
    agree_marketing: bool = Form(False),
    name: Optional[str] = Form(None),
    file: UploadFile = File(None),  # 이미지 파일 추가
) -> Any:
    # 사용자 생성
    user_in = UserCreate(
        username=username,
        password=password,
        nickname=nickname,
        email=email,
        phone_number=phone_number,
        agree_rule=agree_rule,
        agree_marketing=agree_marketing,
        name=name
    )
    res = create_user(session=session, user_create=user_in)
    user = res['db_user']
    token = res['token']

    if file:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        upload_path = get_upload_path('original', file.filename, user.username)
        save_image(file, upload_path)

        thumbnail_path = make_thumbnail(upload_path, size=(350, 350))

        user.profile_image = upload_path
        user.small_image = thumbnail_path
        session.commit()

    return {
        "id": user.id,
        "token": token,
        "profile_image": user.profile_image,
        "small_image": user.small_image,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }

@router.post("/login", response_model=TokenResponse)
def login(
    session: SessionDep,
    username: str = Form(...),
    password: str = Form(...)
):
    user = authenticate_user(session, username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: SessionDep, current_user: CurrentUser):
    user = get_user(session=session, user_id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    is_self(user_id, current_user)
    delete_user_folder(user.username)

    remove_user_from_db(session=session, user=user)
    return {"message": "User deleted successfully"}


@router.put("/users/{user_id}", response_model=UserUpdate)
def update_user_info(
        user_id: int,
        user_update: UserUpdate,
        session: SessionDep, current_user: CurrentUser
):
    is_self(user_id, current_user)
    updated_user = update_user(session=session, user_id=user_id, user_update=user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user

@router.get("/profile", response_model=UserResponse)
def get_user_profile(current_user: CurrentUser):
    return current_user
