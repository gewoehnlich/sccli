from typing import Any
from time import sleep
from pprint import pprint
from requests import Response
from utils.keys import _COLLECTION, _NEXT_HREF
from core.action import Action
from core.request import Request
from core.table import Table


class FetchMyLikedTracksAction(Action):
    def run(
        self,
        request: Request | None = None,
        table:   Table   | None = None,
    ) -> bool:
        if not table:
            raise Exception("no table. to-do later")

        fetched:   bool = False
        next_href: str  = str()

        while not fetched:
            if next_href:
                request: Request = request(url = next_href)
            else:
                request: Request = request()

            response: Response = request.send()
            result: dict[str, Any] = response.json()

            collection: list[dict[str, Any]] = result[_COLLECTION]
            next_href = result[_NEXT_HREF]

            if collection:
                pprint(collection)
                for track in collection:
                    table.insert(track)

            if not next_href:
                fetched = True

            sleep(5)

        # to-do: catch Exceptions

        return True
