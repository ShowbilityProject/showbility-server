# crud/users.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.users import ExtendUser, WithdrawUser
from app.models.tags import Tag
from app.schemas.users import UserCreate, UserUpdate
from app.schemas.tags import TagResponse
from app.core.security import get_password_hash, create_access_token, verify_password
from fastapi import HTTPException, status

def create_user(session: Session, user_create: UserCreate):
    try:
        hashed_password = get_password_hash(user_create.password)
        db_user = ExtendUser(
            username=user_create.username,
            nickname=user_create.nickname,
            hashed_password=hashed_password,
            agree_rule=user_create.agree_rule,
            agree_marketing=user_create.agree_marketing,
            name=user_create.name,
            phone_number=user_create.phone_number,
            email=user_create.email
        )
        if user_create.tags:
            tag_objects = []
            for tag_name in user_create.tags:
                tag = session.query(Tag).filter(Tag.name == tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    session.add(tag)
                    session.commit()
                tag_objects.append(tag)
            db_user.tags = tag_objects

        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        token = create_access_token(user_id=db_user.id)

        return {"db_user": db_user, "token": token}
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="User creation failed: Username or email already exists")

# login
def authenticate_user(session: Session, username: str, password: str):
    user = session.query(ExtendUser).filter(ExtendUser.username == username).first()
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user

def update_user(session: Session, user_id: int, user_update: UserUpdate):
    user = session.query(ExtendUser).filter(ExtendUser.id == user_id).first()
    if not user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key != 'tags':  # 태그는 따로 처리
            setattr(user, key, value)

    # 태그 업데이트
    if user_update.tags:
        tag_objects = []
        for tag in user_update.tags:
            # Tag 객체로 변환 (Pydantic TagResponse가 dict로 되어 있으므로 Tag 객체로 변환 필요)
            tag_object = session.query(Tag).filter(Tag.id == tag.id).first()
            if tag_object:
                tag_objects.append(tag_object)

        # user.tags에 ORM 객체로 저장
        user.tags = tag_objects

    session.commit()
    session.refresh(user)
    return user

def remove_user_from_db(session: Session, user: ExtendUser):
    withdraw_user = WithdrawUser(old_id=user.id, username=user.username)
    session.delete(user)
    session.add(withdraw_user)
    session.commit()

def get_user(session: Session, user_id: int):
    return session.query(ExtendUser).filter(ExtendUser.id == user_id).first()

def get_user_by_email(session: Session, email: str) -> ExtendUser | None:
    return session.query(ExtendUser).filter(ExtendUser.email == email).first()

def get_user_by_id(session: Session, user_id: int) -> ExtendUser | None:
    return session.query(ExtendUser).filter(ExtendUser.id == user_id).first()

def get_user_by_nickname(session: Session, nickname: str):
    return session.query(ExtendUser).filter(ExtendUser.nickname == nickname).first()

def update_password(session: Session, user: ExtendUser, new_password: str) -> ExtendUser:
    user.hashed_password = get_password_hash(new_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# social login
def get_or_create_kakao_user(session: Session, kakao_user_info: dict):
    email = kakao_user_info.get("kakao_account", {}).get("email", "")
    user = None

    if email:
        user = session.query(ExtendUser).filter_by(email=email).first()
        if not user:
            user = ExtendUser(
                username=kakao_user_info['id'],
                email=email,
                login_type="KAKAO"
            )
            session.add(user)
            session.commit()
    else:
        user = session.query(ExtendUser).filter_by(username=kakao_user_info['id']).first()
        if not user:
            user = ExtendUser(
                username=kakao_user_info['id'],
                login_type="KAKAO"
            )
            session.add(user)
            session.commit()

    return user

def get_or_create_apple_user(session: Session, apple_id_token: dict):
    sub = apple_id_token.get('sub')
    email = apple_id_token.get('email')

    user = session.query(ExtendUser).filter(ExtendUser.username == sub).first()
    if not user:
        user = ExtendUser(
            username=sub,
            email=email,
            login_type="APPLE"
        )
        session.add(user)
        session.commit()

    return user

# login 시 response payload handle
def login_user(user: ExtendUser):
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(user_id=user.id)

    response_data = {"token": token, "user": user}

    return response_data