from dependency_injector import containers, providers

from actions.tasks.generate_pkce_task  import GeneratePkceTask
from actions.tasks.generate_state_task import GenerateStateTask


class TasksContainer(
    containers.DeclarativeContainer
):
    generate_pkce = providers.Factory(
        GeneratePkceTask,
    )
    generate_state = providers.Factory(
        GenerateStateTask,
    )
