from pydantic import BaseModel, Field

from settings.tests_database import TestsDatabaseSettings


class TestsSettings(BaseModel):
    database: TestsDatabaseSettings = Field(default_factory=TestsDatabaseSettings)
