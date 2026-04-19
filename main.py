from rich import inspect
from core import di_container
from core.di_container import DiContainer
from core.shell import Shell


def main(
    di_container: DiContainer,
) -> None:
    print(di_container.commands.liked_tracks.run())

    shell = Shell(commands = di_container.commands)
    shell.run()


if __name__ == "__main__":
    di_container: DiContainer = DiContainer()

    di_container.database.initialize_tables()

    main(di_container = di_container)
