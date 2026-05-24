from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    AUTH_POSTGRES_USER: str
    AUTH_POSTGRES_PASSWORD: str
    AUTH_POSTGRES_DB: str
    AUTH_POSTGRES_HOST: str = "localhost"
    AUTH_POSTGRES_PORT: int = 5436

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    APP_TITLE: str = "Auth Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.AUTH_POSTGRES_USER}:{self.AUTH_POSTGRES_PASSWORD}"
            f"@{self.AUTH_POSTGRES_HOST}:{self.AUTH_POSTGRES_PORT}/{self.AUTH_POSTGRES_DB}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"


settings = Settings()