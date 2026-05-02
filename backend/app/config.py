from pathlib import Path

from pydantic_settings import BaseSettings

# Raíz del proyecto (dos niveles arriba de este archivo: config.py → app → backend → raíz)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_ENV_FILE = _PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/evm_tracker"
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = {"env_file": str(_ENV_FILE), "env_file_encoding": "utf-8"}


settings = Settings()
