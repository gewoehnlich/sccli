from config.base_config_model import BaseConfigModel


class DatabaseConfig(BaseConfigModel):
    name: str = "sccli.db"
