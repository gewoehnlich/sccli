from textual.message import Message

from models.track import Track


class TrackSelected(Message):
    def __init__(
        self,
        track: Track,
    ) -> None:
        self.track = track

        super().__init__()
