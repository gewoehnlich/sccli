from pydantic import BaseModel


class ServerSettings(BaseModel):
    port: int = 17874
    path: str = "/callback"
