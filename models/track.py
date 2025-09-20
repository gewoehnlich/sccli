from dependency_injector import providers
from core.model import Model


class Track(
    Model
):
    db  = providers.Dependency()
    dto = providers.Dependency()
