from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.db.database import create_db_and_tables
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description="Auth-сервис с JWT аутентификацией",
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}
