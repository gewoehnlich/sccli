from pydantic import BaseModel, Field


class TestsTokensSettings(BaseModel):
    file: str = Field(default=".test_tokens.json")
