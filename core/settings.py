from pydantic import Field
from pydantic_settings import BaseSettings

from default_settings.database import DatabaseSettings
from default_settings.messages import MessagesSettings
from default_settings.proxy import ProxySettings
from default_settings.server import ServerSettings
from default_settings.soundcloud import SoundcloudSettings
from default_settings.tests import TestsSettings


class Settings(BaseSettings):
    soundcloud: SoundcloudSettings = Field(default_factory=SoundcloudSettings)
    messages: MessagesSettings = Field(default_factory=MessagesSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    server: ServerSettings = Field(default_factory=ServerSettings)
    proxy: ProxySettings = Field(default_factory=ProxySettings)
    tests: TestsSettings = Field(default_factory=TestsSettings)
