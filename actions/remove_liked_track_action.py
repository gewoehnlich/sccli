from dataclasses import dataclass

from core.action import Action
from core.auth import Auth
from core.http_client import HttpClient
from core.request import Request
from core.types import ShellOutputMethod
from exceptions.soundcloud_errors import SoundcloudError
from models.track import Track
from repositories.track_repository import TrackRepository


@dataclass(slots=True, kw_only=True, frozen=True)
class RemoveLikedTrackAction(Action):
    auth: Auth
    http_client: HttpClient
    track_repository: TrackRepository

    async def run(
        self,
        track: Track | None,
        output: ShellOutputMethod | None = None,
    ) -> None:
        if not track:
            return

        await self.http_client.send(
            request=Request(
                method=Request.METHOD.DELETE,
                url=Request.URL.API + f"/likes/tracks/{track.urn}",
                access_token=await self.auth.get_access_token(),
            ),
        )

        await self.track_repository.delete(model=track)

        if output:
            output(f"Removed like from {track.id} - {track.title}")
