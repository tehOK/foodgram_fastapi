from fastapi import APIRouter, Depends, Response

from api_v1.dependencies import validete_auth_user
from core.authentication.utils import encode_jwt
from core.schemas import TokenInfo, UserRead

router = APIRouter(
    tags=["Пользователи"],
    prefix="/token",
)


@router.post("/login/", response_model=TokenInfo)
async def get_token(
    response: Response,
    user: UserRead = Depends(validete_auth_user),
):
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
    }
    token = encode_jwt(jwt_payload)

    response.set_cookie(
        key="auth_token",
        value=token,
        max_age=3600,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )
    return TokenInfo(
        auth_token=token,
    )


@router.post("/logout/")
async def logout():
    pass
