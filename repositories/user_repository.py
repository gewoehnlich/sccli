from typing import Callable
from sqlalchemy.orm import Session

from core.repository import Repository
from models.user import User


class UserRepository(Repository):
    def __init__(
        self,
        model: type[User],
        session_factory: Callable[[], Session],
    ) -> None:
        super().__init__(
            model=model,
            session_factory=session_factory,
        )
