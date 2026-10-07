from pydantic import Field

from config.base_config_model import BaseConfigModel
from config.tests_database import TestsDatabaseConfig


class TestsConfig(BaseConfigModel):
    database: TestsDatabaseConfig = Field(default_factory=TestsDatabaseConfig)
