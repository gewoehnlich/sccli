from typing import Callable
from sqlalchemy.orm import Session

from core.repository import Repository
from models.account import Account


class AccountRepository(Repository):
    def __init__(
        self,
        model: type[Account],
        session_factory: Callable[[], Session],
    ) -> None:
        super().__init__(
            model=model,
            session_factory=session_factory,
        )
