from pydantic import BaseModel


class ProxyConfig(BaseModel):
    endpoint: str = ""
