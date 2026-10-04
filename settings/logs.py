from pathlib import Path

from pydantic_settings import BaseSettings


class LogsSettings(BaseSettings):
    directory: Path = Path("logs")
