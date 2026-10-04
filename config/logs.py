from pathlib import Path

from pydantic_settings import BaseSettings


class LogsConfig(BaseSettings):
    directory: Path = Path("logs")
