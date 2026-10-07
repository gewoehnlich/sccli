from config.base_config_model import BaseConfigModel


class ServerConfig(BaseConfigModel):
    port: int = 8080
    path: str = "/callback"
