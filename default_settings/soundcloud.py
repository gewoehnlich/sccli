from pydantic_settings import BaseSettings


class SoundcloudSettings(BaseSettings):
    client_id:     str = ""
    client_secret: str = ""
