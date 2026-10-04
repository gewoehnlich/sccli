from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    name: str = "sccli.db"
