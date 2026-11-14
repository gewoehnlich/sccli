from collections.abc import AsyncGenerator, Callable, Sequence
from typing import Any

from core.action import Action
from core.auth import Auth
from core.http_client import HttpClient
from core.request import Request
from models.track import Track
from models.user import User
from repositories.track_repository import TrackRepository
from repositories.user_repository import UserRepository


class SyncMyLikedTracksAction(Action):
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

    async def run(self, output: Callable[[str], None] | None = None) -> None:
        existing_users: Sequence[User] = await self.user_repository.get()
        existing_tracks: Sequence[Track] = await self.track_repository.get()

        fetched_users: dict[int, User] = {}
        fetched_tracks: dict[int, Track] = {}

        async for item in self._fetch():
            user: User = User.from_api(data=item["user"])
            track: Track = Track.from_api(data=item, user_id=user.id)

            fetched_users[user.id] = user
            fetched_tracks[track.id] = track

        await self.user_repository.store_many(
            models=list(fetched_users.values()),
        )

        await self.track_repository.store_many(
            models=list(fetched_tracks.values()),
        )

        for user in existing_users:
            if not fetched_users.get(user.id, None):
                await self.user_repository.delete(user)

        for track in existing_tracks:
            if not fetched_tracks.get(track.id, None):
                await self.track_repository.delete(track)

        if output:
            output(f"Synced {len(fetched_tracks)} liked tracks!")

    async def _fetch(self) -> AsyncGenerator[dict[str, Any]]:
        url: str | None = Request.URL.API + "/me/likes/tracks"
        data: dict[str, Any] | None = {
            "limit": 200,
            "access": "playable",
            "linked_partitioning": True,
        }

        while url:
            response: dict[str, Any] = await self.http_client.send(
                request=Request(
                    method=Request.METHOD.GET,
                    url=url,
                    data=data,
                    access_token=await self.auth.get_access_token(),
                ),
            )

            for item in response.get("collection", []):
                yield item

            url = response.get("next_href")
            data = None
