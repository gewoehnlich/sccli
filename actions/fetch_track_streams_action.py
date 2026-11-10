from typing import Any

from core.action import Action
from core.auth import Auth
from core.http_client import HttpClient
from core.request import Request
from models.track import Track
from repositories.track_repository import TrackRepository


class FetchTrackStreamsAction(Action):
    def __init__(
        self,
        auth: Auth,
        http_client: HttpClient,
        track_repository: TrackRepository,
    ) -> None:
        self.auth: Auth = auth
        self.http_client: HttpClient = http_client
        self.track_repository: TrackRepository = track_repository

    async def run(self, track: Track) -> dict[str, Any]:
        request: Request = Request(
            method=Request.METHOD.GET,
            url=Request.URL.API + f"/tracks/{track.urn}/streams",
            access_token=await self.auth.get_access_token(),
        )

        response: dict[str, Any] = await self.http_client.send(request)

        track.streams = response

        await self.track_repository.store(model=track)

        return response
