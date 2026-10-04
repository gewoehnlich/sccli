from pydantic import BaseModel, Field


class TestsDatabaseSettings(BaseModel):
    name: str = Field(default="test.db")
