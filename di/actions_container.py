from actions import fetch_my_liked_tracks_action
from core.di_container import DiContainer


class ActionsContainer(DiContainer):
    def __init__(self) -> None:
        self.fetch_my_liked_tracks = fetch_my_liked_tracks_action
