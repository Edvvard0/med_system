import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # DB_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/data/db.sqlite3"
    DB_URL: str

    API_HOST: str
    API_PORT: int

    LOG_LEVEL: str

    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()
DB_URL = settings.DB_URL
