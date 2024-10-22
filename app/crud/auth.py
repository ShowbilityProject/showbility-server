from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.users import ExtendUser
from app.models.auth import VerificationCode
from app.utils.email_handler import send_mail_with_code
from app.core.security import get_password_hash
import random

def send_verification_code(session: Session, name: str, phone_number: str, email: str):
    user = session.query(ExtendUser).filter_by(name=name, phone_number=phone_number, email=email).first()
    if not user:
        raise ValueError("User not found")

    session.query(VerificationCode).filter_by(user_id=user.id).delete()

    code = send_mail_with_code([user.email])
    verification_code = VerificationCode(user_id=user.id, code=code)
    session.add(verification_code)
    session.commit()

def check_verification_code(session: Session, email: str, code: str) -> str:
    crit_date = datetime.utcnow() - timedelta(minutes=5)

    v_code = session.query(VerificationCode).join(ExtendUser).filter(
        ExtendUser.email == email,
        VerificationCode.code == code,
        VerificationCode.is_valid == True,
        VerificationCode.created_at > crit_date
    ).first()

    if not v_code:
        raise ValueError("Invalid or expired verification code")

    auth_hash = generate_random_hash()
    v_code.auth_hash = auth_hash
    v_code.verified = True
    v_code.is_valid = False
    session.commit()

    return auth_hash

def reset_user_password(session: Session, email: str, new_password: str, auth_hash: str):
    crit_date = make_aware(datetime.now() - timedelta(minutes=20))
    v_code = session.query(VerificationCode).join(ExtendUser).filter(
        ExtendUser.email == email,
        VerificationCode.auth_hash == auth_hash,
        VerificationCode.is_valid == True,
        VerificationCode.verified == True,
        VerificationCode.created_at > crit_date
    ).first()

    if not v_code:
        raise ValueError("인증번호가 다릅니다.")

    user = session.query(ExtendUser).filter(ExtendUser.email == email).first()
    if not user:
        raise ValueError("사용자를 찾을 수 없습니다.")

    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    session.commit()

    session.delete(v_code)
    session.commit()

def is_email_taken(session: Session, email: str) -> bool:
    return session.query(ExtendUser).filter(ExtendUser.email == email).first() is not None

def is_nickname_taken(session: Session, nickname: str) -> bool:
    return session.query(ExtendUser).filter(ExtendUser.nickname == nickname).first() is not None

def generate_random_hash():
    return str(random.getrandbits(128))