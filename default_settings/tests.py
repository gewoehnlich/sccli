from pydantic import BaseModel, Field

from default_settings.tests_database import TestsDatabaseSettings
from default_settings.tests_tokens import TestsTokensSettings


class TestsSettings(BaseModel):
    database: TestsDatabaseSettings = Field(default_factory=TestsDatabaseSettings)
    tokens: TestsTokensSettings = Field(default_factory=TestsTokensSettings)
