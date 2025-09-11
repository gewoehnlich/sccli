from dependency_injector import containers, providers
from actions.fetch_my_liked_tracks_action import FetchMyLikedTracksAction


class ActionsContainer(containers.DeclarativeContainer):
    fetch_my_liked_tracks = providers.Object(FetchMyLikedTracksAction)

    _instance = None

    def __new__(cls) -> None:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance
