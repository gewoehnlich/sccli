from pydantic_settings import BaseSettings


class SoundcloudConfig(BaseSettings):
    client_id: str = ""
    client_secret: str = ""
