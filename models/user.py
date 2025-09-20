from core.model import Model


class User(
    Model
):
    db  = providers.Dependency()
    dto = providers.Dependency()
