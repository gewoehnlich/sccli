from typing import Any, cast

from core.action import Action
from core.auth import Auth
from core.http_client import HttpClient
from core.logger import Logger
from core.player import Player
from core.request import Request
from exceptions.soundcloud_errors import SoundcloudError
from models.track import Track
from repositories.track_repository import TrackRepository


class PlayTrackAction(Action):
    def __init__(
        self,
        auth: Auth,
        http_client: HttpClient,
        player: Player,
        track_repository: TrackRepository,
        logger: Logger,
    ) -> None:
        self.auth: Auth = auth
        self.http_client: HttpClient = http_client
        self.player: Player = player
        self.track_repository: TrackRepository = track_repository
        self.logger: Logger = logger

    async def run(
        self,
        track: Track,
    ) -> Any:
        if not track.streams:
            self.logger.trace(f"no stored streams for track: {track.id} - {track.title}, fetching from API")
            fetched_streams: dict[str, Any] = await self._fetch_track_streams(track=track)

            track.streams = fetched_streams

            track = await self.track_repository.store(model=track)

        streams: dict[str, str] | None = track.streams

        if not streams:
            raise SoundcloudError(
                f"no streams for track {track.id}: {track.title}"
            )

        streaming_url: str = cast(str, streams.get("hls_aac_160_url") or streams.get("hls_mp3_128_url"))

        await self.player.play(link=streaming_url)

    async def _fetch_track_streams(
        self,
        track: Track,
    ) -> dict[str, Any]:
        request: Request = Request(
            method=Request.METHOD.GET,
            url=Request.URL.API + f"/tracks/{track.urn}/streams",
            access_token=await self.auth.get_access_token(),
        )

        response: dict[str, Any] = await self.http_client.send(request)

        return response
