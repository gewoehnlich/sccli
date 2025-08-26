from requests_.get_track_streaming_url_request import GetTrackStreamingUrlRequest
from requests import Response
from pprint import pprint
from utils.send_request import send_request
from typing import List

def get_track_streaming_url_command(args: List[str]) -> None:
    track_urn: str = "soundcloud:tracks:1672134090"
    response: Response = send_request(
        request = GetTrackStreamingUrlRequest(track_urn)
    )

    pprint(response.json())
