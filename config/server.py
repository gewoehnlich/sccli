from pydantic import BaseModel


class ServerConfig(BaseModel):
    port: int = 8080
    path: str = "/callback"
