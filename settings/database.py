from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    name: str = "sccli.db"
