from pathlib import Path

from config.base_config_model import BaseConfigModel


class DatabaseConfig(BaseConfigModel):
    path: Path = Path("sccli.db")
