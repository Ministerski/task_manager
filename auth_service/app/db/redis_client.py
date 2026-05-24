from typing import Optional
import redis as redis_lib
from app.core.config import settings

_redis_client: Optional[redis_lib.Redis] = None


def get_redis_client() -> Optional[redis_lib.Redis]:
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = redis_lib.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                decode_responses=True,
            )
            _redis_client.ping()
        except Exception:
            _redis_client = None
    return _redis_client


def get_redis():
    yield get_redis_client()
