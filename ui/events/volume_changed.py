from textual.message import Message


class VolumeChanged(Message):
    def __init__(
        self,
        volume: int,
    ) -> None:
        self.volume = volume

        super().__init__()
