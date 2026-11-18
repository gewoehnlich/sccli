from core.action import Action
from core.auth import Auth
from core.http_client import HttpClient
from core.request import Request
from core.types import ShellOutputMethod
from models.track import Track
from repositories.track_repository import TrackRepository


class RemoveLikedTrackAction(Action):
    def __init__(
        self,
        auth: Auth,
        http_client: HttpClient,
        track_repository: TrackRepository,
    ) -> None:
        self._auth: Auth = auth
        self._http_client: HttpClient = http_client
        self._track_repository: TrackRepository = track_repository

    async def run(
        self,
        track: Track | None,
        output: ShellOutputMethod | None = None,
    ) -> None:
        if not track:
            return

        await self._http_client.send(
            request=Request(
                method=Request.METHOD.DELETE,
                url=Request.URL.API + f"/likes/tracks/{track.urn}",
                access_token=await self._auth.get_access_token(),
            ),
        )

        await self._track_repository.delete(model=track)

        if output:
            output(f"Removed like from {track.id} - {track.title}")
