from src.core.auth import Auth
from src.core.request import Request
from src.utils.links import SOUNDCLOUD_API_LINK

class GetTrackStreamingUrlRequest(Request):
    def __init__(self, track_urn: str) -> None:
        access_token: str = Auth().get_access_token()
        super().__init__(access_token)

        self.url = SOUNDCLOUD_API_LINK + f"/tracks/{track_urn}/streams"
