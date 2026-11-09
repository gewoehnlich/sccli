from typing import Any, Callable

from core.auth import Auth
from core.command import Command
from core.http_client import HttpClient
from core.request import Request
from exceptions.soundcloud_errors import SoundcloudError
from models.track import Track
from repositories.track_repository import TrackRepository


class RemoveLikedTrackCommand(Command):
    def __init__(
        self,
        auth: Auth,
        http_client: HttpClient,
        track_repository: TrackRepository,
    ) -> None:
        self.auth: Auth = auth
        self.http_client: HttpClient = http_client
        self.track_repository: TrackRepository = track_repository

    async def run(self, track: Track | None, output: Callable[[str], None] | None = None) -> None:
        try:
            if not track:
                return

            response: dict[str, Any] = await self.http_client.send(
                request=Request(
                    method=Request.METHOD.DELETE,
                    url=Request.URL.API + f"/likes/tracks/{track.urn}",
                    access_token=await self.auth.get_access_token(),
                ),
            )

            result: bool = await self.track_repository.delete(
                model=track,
            )

            if output:
                output(f"Removed a like from {track.user.username} - {track.title}")
        except SoundcloudError as e:
            raise e
