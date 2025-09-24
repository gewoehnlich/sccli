from dependency_injector import containers, providers

from models.track_model import TrackModel
from models.user_model import UserModel


class ModelsContainer(
    containers.DeclarativeContainer
):
    track = providers.Singleton(
        TrackModel,
    )
    user = providers.Singleton(
        UserModel,
    )
