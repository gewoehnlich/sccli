from typing import Callable
from sqlalchemy.orm import Session

from core.repository import Repository
from models.track import Track


class TrackRepository(Repository):
    def __init__(
        self,
        model: type[Track],
        session_factory: Callable[[], Session],
    ) -> None:
        super().__init__(
            model=model,
            session_factory=session_factory,
        )
