from pydantic import Field

from config.base_config_model import BaseConfigModel


class TestsDatabaseConfig(BaseConfigModel):
    name: str = Field(default="test.db")
