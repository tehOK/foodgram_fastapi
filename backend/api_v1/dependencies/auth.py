from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import Depends, Form
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from api_v1.crud import UsersCRUD
from auth.utils import decode_jwt, verify_password
from core.models import db_helper
from core.exeptions import ExpireTokenExc, InvalidTokenExc, UnauthorizedExc


http_bearer = HTTPBearer()


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


def get_current_token_payload(
    credentionals: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    token = credentionals.credentials
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
    user = await UsersCRUD.find_by_id(session=session, model_id=user_id)
    if not user:
        raise InvalidTokenExc
    return user
