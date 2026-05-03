from textual.message import Message


class TrackSelected(Message):
    def __init__(
        self,
        urn: str,
    ) -> None:
        self.urn = urn

        super().__init__()
