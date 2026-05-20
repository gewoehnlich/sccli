from core.value import Value
from models.track import Track


class SelectedTrackIndex(Value):
    index: int | None = None

    DEFAULT_VALUE: int = 0

    def value(
        self,
    ) -> int | None:
        return self.index

    def with_value(
        self,
        index: int | None,
    ) -> int | None:
        self.index = index

        return self.value()

    def previous(
        self,
        tracks: list[Track],
    ) -> int | None:
        if len(tracks) <= 0:
            self.index = None

            return self.value()

        if not self.index:
            self.index = self.DEFAULT_VALUE

            return self.value()

        self.index = max(0, self.index - 1)

        return self.value()

    def next(
        self,
        tracks: list[Track],
    ) -> int | None:
        if len(tracks) <= 0:
            self.index = None

            return self.value()

        if not self.index:
            self.index = self.DEFAULT_VALUE

            return self.value()

        self.index = min(len(tracks) - 1, self.index + 1)

        return self.value()
