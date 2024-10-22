from fastapi import APIRouter, HTTPException, Depends
from app.utils.email_handler import send_email
from app.schemas.auth import ResetPasswordRequest, EmailValidationRequest, NicknameValidationRequest
from app.crud.auth import verify_user_code, reset_user_password, is_email_taken, is_nickname_taken
from app.api.deps import SessionDep

router = APIRouter()

@router.post("/request_email_verification")
def request_email_verification(
    email_verification: EmailVerificationRequest,
    session: SessionDep
):
    try:
        send_verification_code(
            session=session,
            name=email_verification.name,
            phone_number=email_verification.phone_number,
            email=email_verification.email
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"message": "인증번호가 전송되었습니다."}

@router.post("/verify_code", response_model=VerifyCodeResponse)
def verify_email_code(
    verify_data: VerifyCodeRequest,
    session: SessionDep
):
    try:
        auth_hash = check_verification_code(
            session=session,
            email=verify_data.email,
            code=verify_data.code
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "인증되었습니다.", "auth_hash": auth_hash}


@router.post("/reset_password")
def reset_password(
    reset_data: ResetPasswordRequest,
    session: SessionDep
):
    try:
        reset_user_password(
            session=session,
            email=reset_data.email,
            new_password=reset_data.password,
            auth_hash=reset_data.auth_hash
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "비밀번호가 재설정되었습니다."}

@router.post("/validate_email")
def validate_email(
    email_data: EmailValidationRequest,
    session: SessionDep
):
    if is_email_taken(session=session, email=email_data.email):
        raise HTTPException(status_code=400, detail="이메일 주소가 이미 사용중입니다.")
    return {"message": "사용 가능한 이메일 주소입니다."}

@router.post("/validate_nickname")
def validate_nickname(
    nickname_data: NicknameValidationRequest,
    session: SessionDep
):
    if is_nickname_taken(session=session, nickname=nickname_data.nickname):
        raise HTTPException(status_code=400, detail="이름이 이미 사용중입니다.")
    return {"message": "사용 가능한 이름입니다."}
