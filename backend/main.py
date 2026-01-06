from contextlib import asynccontextmanager

import uvicorn
from api_v1 import router as api_v1_router
from config import settings
from core.models import db_helper
from fastapi import APIRouter, FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(api_v1_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
