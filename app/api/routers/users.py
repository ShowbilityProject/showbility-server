# app/routers/users.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form, status
from typing import Any, Optional
from app.crud.users import create_user, remove_user_from_db, get_user, authenticate_user, update_user, get_user_by_nickname, get_tags, get_or_create_kakao_user, get_or_create_apple_user, login_user
from app.crud.tags import get_tags
from app.schemas.users import UserSignupResponse, UserCreate, UserResponse, TokenResponse, UserUpdate, KakaoLoginRequest, AppleLoginRequest
from app.api.deps import SessionDep, CurrentUser, is_self
from app.utils.image_handler import get_upload_path, save_image, make_thumbnail, delete_user_folder
from app.models.users import ExtendUser
from app.core.security import create_access_token
from app.core.config import settings

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
            raise HTTPException(status_code=400, detail="파일은 이미지여야 합니다.")

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
        raise HTTPException(status_code=400, detail="접근이 잘못되었습니다.")

    access_token = create_access_token(user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: SessionDep, current_user: CurrentUser):
    user = get_user(session=session, user_id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")

    is_self(user_id, current_user)
    delete_user_folder(user.username)

    remove_user_from_db(session=session, user=user)
    return {"message": "아이디 삭제가 완료되었습니다."}

# 프로필 조회
@router.get("/my", response_model=UserResponse)
def get_user_profile(current_user: CurrentUser):
    return current_user

# 프로필 업데이트
@router.post("/my", response_model=UserUpdate)
def update_user_info(
        session: SessionDep,
        current_user: CurrentUser,
        nickname: Optional[str] = Form(None),
        email: Optional[str] = Form(None),
        phone_number: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        tags: Optional[List[str]] = Form(None),
        file: UploadFile = File(None)
):
    user_update_data = UserUpdate(
        nickname=nickname,
        email=email,
        phone_number=phone_number,
        description=description
    )

    if nickname:
        existing_user = get_user_by_nickname(session=session, nickname=nickname)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=400, detail="닉네임이 이미 사용 중입니다.")

    if file:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="파일은 이미지여야 합니다.")

        upload_path = get_upload_path('original', file.filename, current_user.username)
        save_image(file, upload_path)
        thumbnail_path = make_thumbnail(upload_path, size=(350, 350))

        user_update_data.profile_image = upload_path
        user_update_data.small_image = thumbnail_path

    if tags:
        tag_objects = get_tags(session, tags)
        user_update_data.tags = tag_objects

    updated_user = update_user(session=session, user_id=current_user.id, user_update=user_update_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    return updated_user

# social login
@router.get("/social/kakao")
def redirect_to_kakao():
    kakao_auth_url = f"{settings.KAKAO_GET_AUTH_URL}?response_type=code&client_id={settings.KAKAO_REST_API_KEY}&redirect_uri={settings.KAKAO_REDIRECT_URI}"
    return RedirectResponse(kakao_auth_url)

@router.post("/social/kakao", response_model=TokenResponse)
def kakao_login(kakao_data: KakaoLoginRequest, session: SessionDep):
    access_token = kakao_data.accessToken
    if not access_token:
        raise HTTPException(status_code=400, detail="접근을 위한 토큰이 없습니다.")

    headers = {"Authorization": f"Bearer {access_token}"}
    agreed_info = requests.get(settings.KAKAO_AGREED_INFO_URL, headers=headers)
    user_info = requests.post(settings.KAKAO_USER_INFO_URL, headers=headers).json()

    user = get_or_create_kakao_user(session=session, kakao_user_info=user_info)
    response_data = login_user(user=user, session=session)

    return response_data

@router.post("/social/apple", response_model=TokenResponse)
def apple_login(authorization_code: str = Form(...), session: SessionDep):
    body, verified = apple.Auth.verify_token(authorization_code)
    if not verified:
        raise HTTPException(status_code=400, detail="유효하지 않은 APPLE 인증코드입니다.")

    id_token = apple.Auth.decode_jwt_token(body.get('id_token'))

    user = get_or_create_apple_user(session=session, apple_id_token=id_token)
    response_data = login_user(user=user, session=session)

    return response_data