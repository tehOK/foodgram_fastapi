from typing import Optional

from fastapi import Depends, Form, Response, Request, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError

from api_v1.crud import UsersCRUD
from backend.core.authentication.utils import decode_jwt, verify_password
from core.exeptions import ExpireTokenExc, InvalidTokenExc, UnauthorizedExc
from core.models import db_helper

http_bearer = HTTPBearer(auto_error=False)


async def validete_auth_user(
    email: str = Form(),
    password: str = Form(),
    session=Depends(db_helper.session_getter),
):
    user = await UsersCRUD.find_one_or_none(session=session, email=email)
    if not user:
        raise UnauthorizedExc
    if not verify_password(
        password=password,
        hashed_password=user.password,
    ):
        raise UnauthorizedExc
    return user


async def get_token_from_cookie(request: Request) -> Optional[str]:
    return request.cookies.get("auth_token")


async def get_current_token_payload(
    request: Request,
    credentionals: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    token = None
    if credentionals:
        token = credentionals.credentials
    if not token:
        token = await get_token_from_cookie(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Требуется аутентификация",
                "available_methods": ["bearer_token", "cookie"],
                "documentation": "/docs",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_jwt(
            token=token,
        )
    except ExpiredSignatureError:
        raise ExpireTokenExc
    except InvalidTokenError:
        raise InvalidTokenExc
    return payload


async def get_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session=Depends(db_helper.session_getter),
):
    user_id: str | None = payload.get("sub")
    print(payload)
    user = await UsersCRUD.find_by_id(session=session, model_id=user_id)
    if not user:
        raise InvalidTokenExc
    return user
