from dependency_injector import providers
from core.model import Model


class TrackModel(
    Model
):
    db  = providers.Dependency()
    dto = providers.Dependency()
