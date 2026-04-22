from core.action import Action
from repositories.track_repository import TrackRepository


class GetMyLikedTracksListAction(Action):
    repository: TrackRepository

    def __init__(
        self,
        repository: TrackRepository,
    ) -> None:
        self.repository = repository

    def run() -> dict[str, str]:
        return self.repository.get()
