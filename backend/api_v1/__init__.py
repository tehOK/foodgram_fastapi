from fastapi import APIRouter

from .tags import router as tags_router
from .ingredients import router as ingredients_router
from .users import router as users_router
from .recipes import router as recipes_router
from .auth  import router as auth_router
#from .subscriptions import router as sub_router

router = APIRouter()

router.include_router(tags_router, prefix="/tags")
router.include_router(ingredients_router, prefix="/ingredients")
router.include_router(users_router, prefix="/users")
router.include_router(recipes_router, prefix="/recipes")
router.include_router(auth_router, prefix="/auth")
#router.include_router(sub_router, prefix="/users")
