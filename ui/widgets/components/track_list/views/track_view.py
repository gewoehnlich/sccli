import math
from typing import Any
from core.view import View
from models.track import Track
from models.user import User


class TrackView(View):
    fields: list[str] = [
        'id',
        'username',
        'title',
        'duration',
    ]

    def __init__(
        self,
        track: Track,
        user: User,
    ) -> None:
        self.track = track
        self.user = user

    def view(self) -> tuple[Any]:
        return tuple([
            self.match(field) for field in self.fields
        ])

    def match(
        self,
        field: str,
    ) -> Any:
        match field:
            case 'id':
                return self.id()
            case 'username':
                return self.username()
            case 'title':
                return self.title()
            case 'duration':
                return self.duration()

            case _:
                return None

    def id(self) -> int:
        return self.track.id

    def username(self) -> str:
        return self.user.username

    def title(self) -> str:
        return self.track.title

    def duration(self) -> str:
        milliseconds: int = self.track.duration
        seconds: int = math.ceil(milliseconds / 1000)

        minutes: int = math.floor(seconds / 60)
        seconds %= 60

        return f"{minutes}:{seconds:02d}"
