from pathlib import Path

from config.base_config_model import BaseConfigModel
from enums.logger_level import LoggerLevelEnum


class LogsConfig(BaseConfigModel):
    directory: Path = Path("logs")
    level: LoggerLevelEnum = LoggerLevelEnum.TRACE
