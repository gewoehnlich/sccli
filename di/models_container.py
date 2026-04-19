from core.model     import Model
from models.account import Account
from models.track   import Track
from models.user    import User


class ModelsContainer(

):
    model = Model

    track = Track
    user = User
    account = Account
