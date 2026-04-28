import rich
from sqlalchemy import inspect
from core.di_container import DiContainer
from core.shell import Shell


def main() -> None:
    di_container = DiContainer()
    di_container.database.initialize_tables()
    di_container.logger.info("Starting sccli...")

    di_container.app.run()

    # di_container.logger.info("Running shell...")
    # shell = Shell(commands=di_container.commands)
    # shell.run()


if __name__ == "__main__":
    main()
