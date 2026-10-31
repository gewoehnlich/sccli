from textual.message import Message


class TrackCurrentPlaytimeChanged(Message):
    def __init__(
        self,
        playtime: int,
    ) -> None:
        self.playtime = playtime

        super().__init__()
