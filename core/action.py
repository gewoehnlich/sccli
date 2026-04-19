from abc import abstractmethod
from core.auth import Auth
from core.database import Database
from core.request import Request


class Action(

):
    auth: Auth
    request:  type[Request] | None = None

    def __init__(
        self,
        auth: Auth | None = None,
        request:  type[Request]  | None = None,
        # repository = None,
    ) -> None:
        if auth:
            self.auth = auth

        if request:
            self.request = request

        # if repository:
        #     self.repository = database

    @abstractmethod
    def run(
        self,
    ):
        return None
