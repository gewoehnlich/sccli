from pathlib import Path


from config.base_config_model import BaseConfigModel


class AlembicConfig(BaseConfigModel):
    ini: Path = Path("alembic.ini")
    toml: Path = Path("pyproject.toml")
