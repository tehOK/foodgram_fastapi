from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn

from core.models import db_helper
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()

app = FastAPI(
    lifespan=lifespan
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )