import asyncio
from collections.abc import AsyncGenerator, Callable, Sequence
from typing import Any

from core.auth import Auth
from core.command import Command
from core.http_client import HttpClient
from core.request import Request
from exceptions.soundcloud_errors import SoundcloudError
from models.image import Image
from models.track import Track
from models.user import User
from repositories.image_repository import ImageRepository
from repositories.track_repository import TrackRepository
from repositories.user_repository import UserRepository


class SyncMyLikedTracksCommand(Command):
    def __init__(
        self,
        auth: Auth,
        track_repository: TrackRepository,
        user_repository: UserRepository,
        image_repository: ImageRepository,
        http_client: HttpClient,
    ) -> None:
        self.auth: Auth = auth
        self.track_repository: TrackRepository = track_repository
        self.user_repository: UserRepository = user_repository
        self.image_repository: ImageRepository = image_repository
        self.http_client: HttpClient = http_client

    async def run(self, output: Callable[[str], None] | None = None) -> None:
        users: dict[int, User] = {}
        tracks: dict[int, Track] = {}

        database_tracks: Sequence[Track] = await self.track_repository.get()

        async for item in self._fetch_tracks():
            user: User = User.from_api(data=item["user"])
            track: Track = Track.from_api(data=item, user_id=user.id)

            users[user.id] = user
            tracks[track.id] = track

            if track.artwork_url_large:
                await self._store_image(
                    url=track.artwork_url_large,
                )

        await self.user_repository.store_many(
            models=list(users.values()),
        )

        await self.track_repository.store_many(
            models=list(tracks.values()),
        )

        track_ids = tracks.keys()

        for track in database_tracks:
            if track.id not in track_ids:
                await self.track_repository.delete(track)

        if output:
            output(f"Synced {len(track_ids)} liked tracks!")

    async def _fetch_tracks(self) -> AsyncGenerator[dict[str, Any]]:
        url: str | None = Request.URL.API + "/me/likes/tracks"
        data: dict[str, Any] | None = {
            "limit": 200,
            "access": "playable",
            "linked_partitioning": "true",
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

            if url:
                await asyncio.sleep(0.7)

    async def _store_image(self, url: str) -> None:
        try:
            image: Image | None = await self.image_repository.get_one(
                primary_key=url
            )

            if image:
                return

            data: bytes = await self.http_client.fetch_image(
                request=Request(
                    method=Request.METHOD.GET,
                    url=url,
                    access_token=await self.auth.get_access_token(),
                    headers={
                        "Content-Type": "image/jpeg",
                    },
                ),
            )

            await self.image_repository.store(
                model=Image(
                    url=url,
                    data=data,
                ),
            )
        except SoundcloudError:
            pass
