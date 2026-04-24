from abc import abstractmethod
from typing import Any

from core.auth import Auth
from core.repository import Repository
from core.request import Request


class Action:
    auth: Auth
    request: type[Request]
    repository: Repository

    def __init__(
        self,
        auth: Auth | None = None,
        request: type[Request] | None = None,
        repository: Repository | None = None,
    ) -> None:
        if auth:
            self.auth = auth

        if request:
            self.request = request

        if repository:
            self.repository = repository

    @abstractmethod
    def run(
        self,
    ) -> Any:
        pass
