from fastapi import APIRouter, HTTPException
from app.schemas.users import TokenResponse, KakaoLoginRequest
from app.api.deps import SessionDep
from app.core.config import settings
import requests

router = APIRouter()

@router.get("/user/social_callback", response_model=TokenResponse)
def social_callback(code: str, session: SessionDep):
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.KAKAO_REST_API_KEY,
        "redirect_uri": settings.KAKAO_REDIRECT_URI,
        "code": code
    }

    response = requests.post(settings.KAKAO_GET_TOKEN_URL, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="카카오에서 액세스 토큰을 받는 데 실패했습니다.")

    token_data = response.json()
    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="카카오로부터 액세스 토큰이 제공되지 않았습니다.")

    kakao_data = KakaoLoginRequest(accessToken=access_token)
    kakao_response = requests.post(f"http://127.0.0.1:8000/api/v1/social/kakao", json=kakao_data.model_dump())

    if kakao_response.status_code != 200:
        raise HTTPException(status_code=400, detail="카카오 로그인 처리에 실패했습니다.")

    return kakao_response.json()
