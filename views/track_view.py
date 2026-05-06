from typing import Any

from sqlalchemy import inspect

from core.view import View
from models.track import Track
from repositories.user_repository import UserRepository


class TrackView(View):
    def __init__(
        self,
        fields: list[str],
        user_repository: UserRepository,
    ) -> None:
        self.fields = fields
        self.user_repository = user_repository

    def to_tuple(
        self,
        track: Track,
    ) -> tuple[Any]:
        data: dict[str, Any] = {}

        for attr in inspect(track).mapper.column_attrs:
            data[attr.key] = getattr(track, attr.key)

        print(data)
        if 'user_id.username' in self.fields:
            data['username'] = self.user_repository.get(
                id=data['user_id'],
            )[0].username

            self.fields[self.fields.index('user_id.username')] = 'username'

        return tuple(data[field] for field in self.fields)
