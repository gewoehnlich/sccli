from pathlib import Path

from pydantic import Field

from config.alembic import AlembicConfig
from config.base_config_model import BaseConfigModel


class DatabaseConfig(BaseConfigModel):
    path: Path = Path("sccli.db")

    alembic: AlembicConfig = Field(default_factory=AlembicConfig)
