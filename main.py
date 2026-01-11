from dependency_injector.wiring import Provide, inject
from rich import inspect

from core.di_container      import DiContainer
from core.settings          import Settings
# from core.shell import Shell
from default_settings.app   import AppSettings


@inject
def main(
    di_container: DiContainer = Provide[DiContainer],
) -> None:
    print(di_container.auth().get_access_token())
    print(123)
    # Shell().run()
    # di_container.commands().welcome().run()
    # di_container.commands().my_liked_tracks().run()


if __name__ == "__main__":
    settings: AppSettings = Settings().load()

    di_container: DiContainer = DiContainer()
    di_container.config.from_pydantic(
        settings = settings,
    )

    di_container.database().initialize_tables()

    di_container.wire(
        modules = [__name__],
    )

    main()
