from dependency_injector.wiring import Provide

from core.di_container import DiContainer
from core.settings import Settings
from default_settings.app import AppSettings
# from core.shell import Shell


def main(di_container: DiContainer = Provide[DiContainer]) -> None:
    di_container.commands().welcome().run()
    di_container.commands().my_liked_tracks().run()


if __name__ == "__main__":
    settings: AppSettings = Settings().load()

    di_container: DiContainer = DiContainer()
    di_container.config.from_pydantic(settings)

    di_container.db().initialize_tables()

    di_container.wire(modules = [__name__])

    # main()
    print(
        di_container.auth().get_access_token()
    )
