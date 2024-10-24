from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

# from app.models.groups import GroupMember
# from app.models.contents import Content
from app.db.engine import get_db
from app.models.users import ExtendUser
from app.core.config import settings

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

from app.core.config import settings  # 설정 파일에서 secret key와 알고리즘 불러오기

def get_current_user(session: SessionDep, token: TokenDep) -> ExtendUser:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    user = session.get(ExtendUser, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

CurrentUser = Annotated[ExtendUser, Depends(get_current_user)]

def is_self(user_id: int, current_user: CurrentUser) -> bool:
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 없습니다. 본인이 아닙니다."
        )
    return True
#
# def is_content_owner(
#     content_id: int, session: SessionDep, current_user: CurrentUser
# ) -> bool:
#     content = session.query(Content).filter_by(id=content_id).first()
#
#     if content is None or content.user_id != current_user.id:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="권한이 없습니다. 콘텐츠 소유자가 아닙니다."
#         )
#
#     return True
#

# def is_group_manager(
#     group_id: int, session: SessionDep, current_user: CurrentUser
# ) -> bool:
#     group_member = session.query(GroupMember).filter_by(
#         group_id=group_id, user_id=current_user.id
#     ).first()
#
#     if not group_member or group_member.member_type not in [GroupMember.MemberType.LEADER, GroupMember.MemberType.MANAGER]:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="권한이 없습니다. 그룹 관리자가 아닙니다."
#         )
#
#     return True


def permission_required(action: str):
    def permissions_check(
        user_id: int = None, current_user: CurrentUser = Depends(get_current_user)
    ):
        no_permission_actions = [
            'create', 'retrieve', 'social', 'social_callback', 'kakao', 'apple',
            'validate_email', 'validate_nickname', 'request_email_verification',
            'verify_code', 'reset_password'
        ]

        if action in no_permission_actions:
            return  # 권한 체크 없음
        elif action in ['destroy', 'update']:
            # destroy 또는 update의 경우 IsAuthenticated + IsSelf 체크
            if user_id:
                return is_self(user_id, current_user)
        else:
            # 그 외의 경우는 IsAuthenticated 체크
            return current_user

    return permissions_check
