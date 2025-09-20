from dependency_injector import providers
from core.model import Model


class UserModel(
    Model
):
    db  = providers.Dependency()
    dto = providers.Dependency()
