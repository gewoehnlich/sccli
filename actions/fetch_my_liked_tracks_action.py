from requests import Response
from core.action import Action
from core.request import Request
from core.table import Table
from requests_.fetch_my_liked_tracks_request import FetchMyLikedTracksRequest
from tables.tracks import TracksTable
from utils.send_request import send_request
from typing import Any
from time import sleep
from pprint import pprint
from utils.keys import _COLLECTION, _NEXT_HREF

class FetchMyLikedTracksAction(Action):
    def run(
        self,
        # request: Request,
        table: Table | None = None,
    ) -> bool:
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

            collection: list[dict[str, Any]] = result[_COLLECTION]
            next_href = result[_NEXT_HREF]

            if collection:
                pprint(collection)
                # for track in collection:
                #     table.insert(track)

            if not next_href:
                fetched = True

            sleep(5)

        # to-do: catch Exceptions

        return True
