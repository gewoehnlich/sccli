from dependency_injector import containers, providers

from core.model     import Model
from models.account import Account
from models.track   import Track
from models.user    import User


class ModelsContainer(
    containers.DeclarativeContainer
):
    model = providers.Singleton(
        Model,
    )

    track = providers.Singleton(
        Track,
    )
    user = providers.Singleton(
        User,
    )
    account = providers.Singleton(
        Account,
    )
