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
    description="Сервис управления задачами. Требует JWT токен от Auth Service.",
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "tasks", "version": settings.APP_VERSION}
