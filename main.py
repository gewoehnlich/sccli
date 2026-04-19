from rich import inspect
from core import di_container
from core.di_container import DiContainer


def main(
    di_container: DiContainer,
) -> None:
    # print(di_container.auth.get_access_token())
    print(di_container.commands.welcome.run())


if __name__ == "__main__":
    di_container: DiContainer = DiContainer()

    di_container.database.initialize_tables()

    main(
        di_container = di_container,
    )
