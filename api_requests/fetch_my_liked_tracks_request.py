from typing import Any
from core.requests.soundcloud_request import SoundcloudRequest


class FetchMyLikedTracksRequest(SoundcloudRequest):
    def __init__(
        self,
        access_token: str,
        url: str | None = None,
    ) -> None:
        if not url:
            url = self.SOUNDCLOUD_API_LINK + "/me/likes/tracks"

        params: dict[str, Any] = {
            "limit": 50,
            "access": "playable",
            "linked_partitioning": True,
        }

        super().__init__(
            method="GET",
            url=url,
            params=params,
            access_token=access_token,
        )
