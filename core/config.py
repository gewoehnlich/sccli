import sys
import yaml
from typing import Any
from pydantic import ValidationError

from default_settings.app import AppSettings
from exceptions.client_id_is_not_set_exception import ClientIdIsNotSetException
from exceptions.client_secret_is_not_set_exception import ClientSecretIsNotSetException


class Config:
    CONFIG_PATH: str = "config.yml"

    def load(
        self,
    ) -> AppSettings:
        user_config_data: dict[str, Any] = self.__read_user_config_data()

        self.__ensure_client_credentials_are_set(
            config_data=user_config_data,
        )

        filtered_config: dict[str, Any] = self.__remove_none_values(
            config=user_config_data
        )

        settings: AppSettings = self.__add_default_values(config=filtered_config)

        return settings

    def __read_user_config_data(
        self,
    ) -> dict[str, Any]:
        with open(file=self.CONFIG_PATH, mode="r", encoding="utf-8") as f:
            user_config_data = yaml.safe_load(f)

        return user_config_data

    def __ensure_client_credentials_are_set(
        self,
        config_data: dict[str, Any],
    ) -> None:
        client_id = config_data["soundcloud"]["client_id"]
        if not isinstance(client_id, str) or not client_id:
            raise ClientIdIsNotSetException

        client_secret = config_data["soundcloud"]["client_secret"]
        if not isinstance(client_secret, str) or not client_secret:
            raise ClientSecretIsNotSetException

    def __remove_none_values(
        self,
        config: dict[str, Any],
    ) -> dict[str, Any]:
        if isinstance(config, dict):
            return {
                key: self.__remove_none_values(value)
                for key, value in config.items()
                if value is not None
            }

        return config

    def __add_default_values(
        self,
        config: dict[str, Any],
    ) -> AppSettings:
        try:
            settings = AppSettings.model_validate(config)
        except ValidationError as e:
            print(
                f"ERROR: Invalid configuration in '{self.CONFIG_PATH}':\n{e}",
                file=sys.stderr,
            )
            sys.exit(1)

        return settings
