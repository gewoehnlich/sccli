from typing import Any, Self
from time   import sleep
from pprint import pprint
from requests import Response
from rich import inspect

from api_requests.fetch_my_liked_tracks_request import FetchMyLikedTracksRequest
from core.auth import Auth
from core.database            import Database
from core.action              import Action
from core.request             import Request
from enums.response_keys_enum import ResponseKeysEnum


class FetchMyLikedTracksAction(
    Action
):
    def __init__(
        self,
        auth: Auth,
        request: type[Request],
    ) -> None:
        super().__init__(
            auth = auth,
            request = request,
        )


    def run(
        self,
    ) -> bool:
        request_factory = self.request
        inspect(request_factory)

        if not request_factory:
            raise Exception("no table. to-do later")

        fetched:   bool = False
        next_href: str  = str()

        while not fetched:
            if next_href:
                request: Request = request_factory(
                    access_token = self.auth.get_access_token(),
                    url = next_href,
                )
            else:
                request: Request = request_factory(
                    access_token = self.auth.get_access_token(),
                )

            response: dict[str, dict[str, str | int] | str] = request.send()

            collection: list[dict[str, Any]] = response['collection']
            next_href = response['next_href']

            if collection:
                pprint(collection)
                for track in collection:
                    self.database.insert(
                        table = table,
                        data = track,
                    )

            if not next_href:
                fetched = True

            sleep(5)

        # to-do: catch Exceptions

        return True
