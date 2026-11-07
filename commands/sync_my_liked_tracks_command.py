from collections.abc import Callable, Generator, Sequence
from time import sleep
from typing import Any

from core.auth import Auth
from core.command import Command
from core.http_client import HttpClient
from core.request import Request
from models.track import Track
from models.user import User
from repositories.track_repository import TrackRepository
from repositories.user_repository import UserRepository


class SyncMyLikedTracksCommand(Command):
    def __init__(
        self,
        auth: Auth,
        track_repository: TrackRepository,
        user_repository: UserRepository,
        http_client: HttpClient,
    ) -> None:
        self.auth: Auth = auth
        self.track_repository: TrackRepository = track_repository
        self.user_repository: UserRepository = user_repository
        self.http_client: HttpClient = http_client

    def run(self, output: Callable[[str], None] | None = None) -> None:
        users: dict[int, User] = {}
        tracks: dict[int, Track] = {}

        database_tracks: Sequence[Track] = self.track_repository.get()

        for item in self._fetch_tracks():
            user: User = User.from_api(data=item["user"])
            track: Track = Track.from_api(data=item, user_id=user.id)

            users[user.id] = user
            tracks[track.id] = track

        self.user_repository.store_many(
            models=list(users.values())
        )

        self.track_repository.store_many(
            models=list(tracks.values())
        )

        track_ids = tracks.keys()

        for track in database_tracks:
            if track.id not in track_ids:
                self.track_repository.delete(track)

        if output:
            output(f"Synced {len(track_ids)} liked tracks!")

    def _fetch_tracks(self) -> Generator[dict[str, Any]]:
        url: str | None = Request.URL.API + "/me/likes/tracks"
        data: dict[str, Any] | None = {
            "limit": 200,
            "access": "playable",
            "linked_partitioning": "true",
        }

        while url:
            response: dict[str, Any] = self.http_client.send(
                request=Request(
                    method=Request.METHOD.GET,
                    url=url,
                    data=data,
                    access_token=self.auth.get_access_token(),
                ),
            )

            yield from response.get("collection", [])

            url = response.get("next_href")
            data = None

            if url:
                sleep(0.7)
