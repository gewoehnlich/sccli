from pydantic import BaseModel


class ServerSettings(BaseModel):
    port: int = 8080
    path: str = "/callback"
