from fastapi import APIRouter, HTTPException, Depends
from app.utils.email_handler import send_email
from app.core.security import create_access_token, verify_password, get_password_hash, decode_access_token
from app.schemas.users import UserCreate
from app.crud.users import create_user, get_user_by_email, update_password, get_user_by_id
from app.api.deps import SessionDep


router = APIRouter()


@router.post("/register")
def register_user(user_create: UserCreate, session: SessionDep):
    existing_user = get_user_by_email(session=session, email=user_create.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = create_user(session=session, user_create=user_create)

    token = create_access_token(user_id=user.id)
    activation_link = f"http://showbility.com/activate/{token}" # 변경해줘야함

    send_email(
        subject="Activate your account",
        recipient=user.email,
        body=f"Click the link to activate your account: {activation_link}"
    )

    return {"message": "Registration successful! Please check your email to activate your account."}


@router.get("/activate/{token}")
def activate_user(token: str, session: SessionDep):
    user_id = decode_access_token(token)
    user = get_user_by_id(session=session, user_id=user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    session.commit()

    return {"message": "Account activated successfully"}

@router.post("/password-reset-request")
def password_reset_request(email: str, session: SessionDep):
    user = get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_access_token(user_id=user.id)
    reset_link = f"http://showbility.com/reset-password/{token}" # 수정 필요

    send_email(
        subject="Reset your password",
        recipient=user.email,
        body=f"Click the link to reset your password: {reset_link}"
    )

    return {"message": "Password reset email sent!"}

@router.post("/reset-password/{token}")
def reset_password(token: str, new_password: str, session: SessionDep):
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_password(session, user, new_password)
    return {"msg": "Password updated successfully"}
