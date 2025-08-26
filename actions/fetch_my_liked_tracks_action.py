from requests import Response
from core.action import Action
from requests_.fetch_my_liked_tracks_request import FetchMyLikedTracksRequest
from utils.send_request import send_request
from typing import Any
from time import sleep
from pprint import pprint

class FetchMyLikedTracksAction(Action):
    _COLLECTION: str = "collection"
    _NEXT_HREF: str  = "next_href"

    def run(self) -> bool:
        fetched: bool = False
        next_href: str = str()

        while not fetched:
            if next_href:
                request: FetchMyLikedTracksRequest = FetchMyLikedTracksRequest(
                    url = next_href
                )
            else:
                request: FetchMyLikedTracksRequest = FetchMyLikedTracksRequest()
        
            response: Response = send_request(request = request)
            result: dict[str, Any] = response.json()

            collection: dict[str, Any] = result[self._COLLECTION]
            next_href = result[self._NEXT_HREF]

            if collection:
                pprint(collection)

            if next_href:
                pprint(next_href)

            if not next_href:
                fetched = True

            sleep(5)

        # to-do: catch Exceptions

        return True
