from collections.abc import Sequence
from random import randrange

from core.value import Value
from exceptions.playlist_errors import (
    PlaylistEmptyError,
    PlaylistInvalidIndexError,
)
from models.track import Track


class Playlist(Value):
    def __init__(
        self,
        tracks: Sequence[Track],
        index: int | None = None,
    ) -> None:
        self.tracks: Sequence[Track] = tracks

        if index is None:
            index = 0 if self.tracks else None
        elif not 0 <= index < len(self.tracks):
            raise PlaylistInvalidIndexError

        self.index: int | None = index

    def current(
        self,
    ) -> Track | None:
        if self.index is None:
            return None

        return self.tracks[self.index]

    def select(
        self,
        index: int,
    ) -> Track:
        if not 0 <= index < len(self.tracks):
            raise PlaylistInvalidIndexError

        self.index = index

        return self.tracks[index]

    def next(self) -> Track:
        return self.random()
        # return self._move(step=1)

    def prev(self) -> Track:
        return self._move(step=-1)

    def random(self) -> Track:
        index = self._require_index()

        if len(self.tracks) == 1:
            return self.select(0)

        new_index = randrange(len(self.tracks) - 1)

        if new_index >= index:
            new_index += 1

        return self.select(new_index)

    def _move(self, step: int) -> Track:
        index = self._require_index()

        return self.select((index + step) % len(self.tracks))

    def _require_index(self) -> int:
        if self.index is None:
            raise PlaylistEmptyError

        return self.index

    def __len__(self) -> int:
        return len(self.tracks)
