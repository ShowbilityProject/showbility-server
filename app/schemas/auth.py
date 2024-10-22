from pydantic import BaseModel, EmailStr

class EmailVerificationRequest(BaseModel):
    name: str
    phone_number: str
    email: EmailStr

class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str

class VerifyCodeResponse(BaseModel):
    message: str
    auth_hash: str

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    password: str
    auth_hash: str

class EmailValidationRequest(BaseModel):
    email: EmailStr

class NicknameValidationRequest(BaseModel):
    nickname: str