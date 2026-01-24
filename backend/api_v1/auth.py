from fastapi import APIRouter, Depends

from api_v1.dependencies import validete_auth_user
from core.authentication.utils import encode_jwt
from core.schemas import TokenInfo, UserRead

router = APIRouter(
    tags=["Пользователи"],
    prefix="/token",
)


@router.post("/login/", response_model=TokenInfo)
async def get_token(
    user: UserRead = Depends(validete_auth_user),
):
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
    }
    token = encode_jwt(jwt_payload)
    return TokenInfo(
        auth_token=token,
    )


@router.post("/logout/")
async def logout():
    pass
