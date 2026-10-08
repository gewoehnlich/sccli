import sys
from pathlib import Path

from core.di_container import DiContainer
from exceptions.config.config_error import ConfigError
from ui.app import App


def main() -> int:
    try:
        di_container: DiContainer = DiContainer(
            config_file=Path("config.yml"),
        )

        di_container.database.initialize_tables()
        di_container.logger.info("Starting sccli...")

        app = App(di_container=di_container)
        app.run()
    except ConfigError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    main()
