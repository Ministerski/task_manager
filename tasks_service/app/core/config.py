from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    TASKS_POSTGRES_USER: str
    TASKS_POSTGRES_PASSWORD: str
    TASKS_POSTGRES_DB: str
    TASKS_POSTGRES_HOST: str = "localhost"
    TASKS_POSTGRES_PORT: int = 5435

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    AUTH_SERVICE_URL: str = "http://localhost:8000"

    APP_TITLE: str = "Tasks Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.TASKS_POSTGRES_USER}:{self.TASKS_POSTGRES_PASSWORD}"
            f"@{self.TASKS_POSTGRES_HOST}:{self.TASKS_POSTGRES_PORT}/{self.TASKS_POSTGRES_DB}"
        )


settings = Settings()