from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from default_settings.database import DatabaseSettings
from default_settings.messages import MessagesSettings
from default_settings.server import ServerSettings
from default_settings.soundcloud import SoundcloudSettings
from default_settings.tests import TestsSettings
from default_settings.tokens import TokensSettings


class AppSettings(BaseSettings):
    soundcloud: SoundcloudSettings = Field(
        default_factory = SoundcloudSettings
    )
    messages: MessagesSettings = Field(
        default_factory = MessagesSettings
    )
    tokens: TokensSettings = Field(
        default_factory = TokensSettings
    )
    database: DatabaseSettings = Field(
        default_factory = DatabaseSettings
    )
    server: ServerSettings = Field(
        default_factory = ServerSettings
    )
    tests: TestsSettings = Field(
        default_factory = TestsSettings
    )
