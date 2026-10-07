from config.base_config_model import BaseConfigModel


class ProxyConfig(BaseConfigModel):
    endpoint: str | None = None
