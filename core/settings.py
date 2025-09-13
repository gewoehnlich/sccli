import sys
import yaml
from typing import Any, Self
from pydantic import BaseModel, ValidationError

from default_settings.app import AppSettings


class Settings():
    CONFIG_PATH: str = "config.yml"

    _instance:    Self | None = None
    _initialized: bool        = False


    def __new__(
        cls: type[Self],
        *args,
        **kwargs
    ) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance


    def __init__(
        self
    ) -> None:
        if self._initialized:
            return

        super().__init__()

        self._initialized = True


    def load(
        self,
    ) -> AppSettings:
        user_config_data: dict[str, Any] = self.read_user_config_data()
        filtered_config: dict[str, Any] = self.remove_none_values(
            config = user_config_data
        )
        settings: AppSettings = self.add_default_values(
            config = filtered_config
        )

        return settings


    def read_user_config_data(
        self,
    ) -> dict[str, Any]:
        try:
            with open(
                file = self.CONFIG_PATH,
                mode = "r",
                encoding = "utf-8"
            ) as f:
                user_config_data = yaml.safe_load(f) or {}

        # throw an error
        except FileNotFoundError:
            print(f"INFO: '{ self.CONFIG_PATH }' not found. Using default settings.")
            user_config_data = {}

        return user_config_data


    def remove_none_values(
        self,
        config: dict[str, Any] | None,
    ) -> dict[str, Any] | None:
        if isinstance(config, dict):
            return {
                key: self.remove_none_values(value)
                for key, value in config.items()
                if value is not None
            }

        return config


    def add_default_values(
        self,
        config: dict[str, Any],
    ) -> AppSettings:
        try:
            settings = AppSettings.model_validate(config)

        except ValidationError as e:
            print(f"ERROR: Invalid configuration in '{ CONFIG_PATH }':\n{e}", file=sys.stderr)
            sys.exit(1)

        return settings
