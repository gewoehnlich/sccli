from dependency_injector import containers, providers

from models.track_model import TrackModel
from models.user_model import UserModel


class ModelsContainer(
    containers.DeclarativeContainer
):
    db_models  = providers.DependenciesContainer()
    dto_models = providers.DependenciesContainer()

    track = providers.Singleton(
        TrackModel,
        db  = db_models.tracks,
        dto = dto_models.track,
    )
    user = providers.Singleton(
        UserModel,
        db  = db_models.users,
        dto = dto_models.user,
    )
