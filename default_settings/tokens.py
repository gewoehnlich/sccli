from pydantic_settings import BaseSettings


class TokensSettings(BaseSettings):
    file: str = ".tokens.json"
