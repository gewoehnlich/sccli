from pydantic import BaseModel, Field

from config.tests_database import TestsDatabaseConfig


class TestsConfig(BaseModel):
    database: TestsDatabaseConfig = Field(default_factory=TestsDatabaseConfig)
