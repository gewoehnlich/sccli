from pathlib import Path

from config.base_config_model import BaseConfigModel


class LogsConfig(BaseConfigModel):
    directory: Path = Path("logs")
