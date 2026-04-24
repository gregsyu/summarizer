from pydantic import BaseSettings, SettingsConfigDict
from typing import List
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local", ".env.development"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    MODEL: str = os.getenv("MODEL")
    BASE_URL: str = os.getenv("BASE_URL")
    ALLOW_ORIGINS: List[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]

settings = Settings()
