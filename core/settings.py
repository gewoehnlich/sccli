from pydantic import Field
from pydantic_settings import BaseSettings

from settings.database import DatabaseSettings
from settings.logs import LogsSettings
from settings.messages import MessagesSettings
from settings.proxy import ProxySettings
from settings.server import ServerSettings
from settings.soundcloud import SoundcloudSettings
from settings.tests import TestsSettings


class Settings(BaseSettings):
    soundcloud: SoundcloudSettings = Field(default_factory=SoundcloudSettings)
    messages: MessagesSettings = Field(default_factory=MessagesSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    server: ServerSettings = Field(default_factory=ServerSettings)
    proxy: ProxySettings = Field(default_factory=ProxySettings)
    tests: TestsSettings = Field(default_factory=TestsSettings)
    logs: LogsSettings = Field(default_factory=LogsSettings)
