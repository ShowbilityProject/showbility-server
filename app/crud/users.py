# crud/users.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.users import ExtendUser, WithdrawUser#, UserUpdate
from app.schemas.users import UserCreate
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
        session.add(db_user)
        session.commit()
        session.refresh(db_user)


        token = create_access_token(user_id=db_user.id)

        return {"db_user": db_user, "token": token}
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="User creation failed: Username or email already exists")

def authenticate_user(session: Session, username: str, password: str):
    user = session.query(ExtendUser).filter(ExtendUser.username == username).first()
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

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

def update_password(session: Session, user: ExtendUser, new_password: str) -> ExtendUser:
    user.hashed_password = get_password_hash(new_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user