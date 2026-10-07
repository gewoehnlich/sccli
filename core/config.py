from pydantic import Field

from config.base_config_model import BaseConfigModel
from config.database import DatabaseConfig
from config.logs import LogsConfig
from config.messages import MessagesConfig
from config.proxy import ProxyConfig
from config.server import ServerConfig
from config.soundcloud import SoundcloudConfig
from config.tests import TestsConfig


class Config(BaseConfigModel):
    soundcloud: SoundcloudConfig
    messages: MessagesConfig = Field(default_factory=MessagesConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)
    proxy: ProxyConfig = Field(default_factory=ProxyConfig)
    tests: TestsConfig = Field(default_factory=TestsConfig)
    logs: LogsConfig = Field(default_factory=LogsConfig)
