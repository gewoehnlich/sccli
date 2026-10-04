from pydantic import BaseModel, Field


class TestsDatabaseConfig(BaseModel):
    name: str = Field(default="test.db")
