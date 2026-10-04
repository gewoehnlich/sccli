from pydantic import BaseModel


class ProxySettings(BaseModel):
    endpoint: str = ""
