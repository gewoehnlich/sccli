from dependency_injector.wiring import Provide, inject

from core.settings          import Settings
from default_settings.app   import AppSettings
from di.actions_container   import ActionsContainer
from di.commands_container  import CommandsContainer
from di.config_container    import ConfigContainer
from di.dto_container       import DtoContainer
from di.models_container    import ModelsContainer
from di.requests_container  import RequestsContainer
from di.resources_container import ResourcesContainer
from di.tables_container    import TablesContainer
# from core.shell import Shell


@inject
def main(
    commands: CommandsContainer = Provide[CommandsContainer],
) -> None:
    commands.welcome().run()
    # di_container.commands().my_liked_tracks().run()


if __name__ == "__main__":
    settings: AppSettings = Settings().load()

    actions:    ActionsContainer    = ActionsContainer()
    commands:   CommandsContainer   = CommandsContainer()
    config:     ConfigContainer     = ConfigContainer()
    dto:        DtoContainer        = DtoContainer()
    models:     ModelsContainer     = ModelsContainer()
    requests:   RequestsContainer   = RequestsContainer()
    resources:  ResourcesContainer  = ResourcesContainer()
    tables:     TablesContainer     = TablesContainer()

    config.config.from_pydantic(
        settings = settings,
    )

    di_container.database().initialize_tables()

    di_container.wire(
        modules = [__name__],
    )

    main()
