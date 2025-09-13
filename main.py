import sys
import yaml
from dependency_injector.wiring import Provide
from pydantic import ValidationError

from core.di_container import DiContainer
from default_settings.app import AppSettings
# from core.shell import Shell


def remove_none_values(config):
    """Recursively remove keys with None values from a dictionary."""
    if isinstance(config, dict):
        return {
            key: remove_none_values(value)
            for key, value in config.items()
            if value is not None
        }
    if isinstance(config, list):
        return [remove_none_values(item) for item in config]
    return config


def main(di_container: DiContainer = Provide[DiContainer]) -> None:
    di_container.commands().welcome().run()
    # di_container.commands().my_liked_tracks().run()


if __name__ == "__main__":
    CONFIG_PATH: str = "config.yml"

    try:
        with open(
            file = CONFIG_PATH,
            mode = "r",
            encoding = "utf-8"
        ) as f:
            user_config_data = yaml.safe_load(f) or {}

    except FileNotFoundError:
        print(f"INFO: '{ CONFIG_PATH }' not found. Using default settings.")
        user_config_data = {}

    # Filter out None values so Pydantic can apply defaults
    filtered_config = remove_none_values(user_config_data)

    try:
        settings = AppSettings.model_validate(filtered_config)
        print(settings)

    except ValidationError as e:
        print(f"ERROR: Invalid configuration in '{ CONFIG_PATH }':\n{e}", file=sys.stderr)
        sys.exit(1)

    sys.exit(1)

    di_container: DiContainer = DiContainer()

    di_container.config.from_pydantic(settings)

    di_container.db().initialize_tables()
    di_container.wire(modules=[__name__])

    main()
