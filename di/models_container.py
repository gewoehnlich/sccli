from dependency_injector import containers, providers

from models.track import Track
from models.user import User


class ModelsContainer(
    containers.DeclarativeContainer
):
    track = providers.Singleton(
        Track,
    )
    user = providers.Singleton(
        User,
    )
