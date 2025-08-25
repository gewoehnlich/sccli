from src.requests.users_liked_tracks_request import UsersLikedTracksRequest 
from requests import Response
from pprint import pprint
from src.utils.send_request import send_request
from typing import List, Any

def users_liked_tracks_command(args: List[str]) -> None:
    _COLLECTION = "collection"
    _NEXT_HREF  = "next_href"

    request: UsersLikedTracksRequest = UsersLikedTracksRequest()
    response: Response = send_request(request = request)

    result: dict[str, Any] = response.json()

    collection: dict[str, Any] = result[_COLLECTION]
    next_href: str | None = result[_NEXT_HREF]

    if collection:
        pprint(collection)

    if next_href:
        pprint(next_href)
