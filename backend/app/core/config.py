from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "Private Blog API"
    api_prefix: str = "/api"
    frontend_origin: str = "http://localhost:5173"
    database_url: str = f"sqlite:///{BASE_DIR / 'data' / 'private-blog.db'}"
    jwt_secret_key: str = "change-this-private-blog-secret"
    jwt_expire_minutes: int = 60 * 24 * 7
    static_dir: Path = BASE_DIR / "static"
    upload_dir: Path = BASE_DIR / "static" / "uploads"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8")


@lru_cache
def getSettings() -> Settings:
    return Settings()
