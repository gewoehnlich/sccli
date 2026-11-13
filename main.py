import asyncio
import sys
from pathlib import Path

from core.di_container import DiContainer
from exceptions.config.config_error import ConfigError
from ui.app import App


async def main() -> int:
    try:
        di_container: DiContainer = DiContainer(
            config_file=Path("config.yml"),
        )
        di_container.wire(packages=["ui"])

        await asyncio.to_thread(di_container.database().run_migrations)

        await App().run_async()
    except ConfigError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
