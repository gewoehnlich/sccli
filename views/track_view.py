from typing import Any

from sqlalchemy import inspect

from core.view import View
from models.track import Track


class TrackView(View):
    def __init__(
        self,
        fields: list[str],
    ) -> None:
        self.fields = fields

    def to_tuple(
        self,
        track: Track,
    ) -> tuple[Any]:
        data: dict[str, Any] = {}

        for attr in inspect(track).mapper.column_attrs:
            if attr.key not in self.fields:
                continue

            data[attr.key] = getattr(track, attr.key)

        return tuple(data[field] for field in self.fields)
