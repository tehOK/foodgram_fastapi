

from fastapi import APIRouter

router = APIRouter(
    tags=["Пользователи"],
    prefix="/token",
)

@router.post("/login/")
async def get_token():
    pass

@router.post("/logout/")
async def logout():
    pass