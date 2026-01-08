from typing import Any, Self
from time   import sleep
from pprint import pprint
from dependency_injector.wiring import Provide, inject
from requests import Response

from core.database            import Database
from core.action              import Action
from core.request             import Request
from core.table               import Table
from enums.response_keys_enum import ResponseKeysEnum


class FetchMyLikedTracksAction(
    Action
):
    _instance:    Self | None = None
    _initialized: bool        = False

    def __new__(
        cls: type[Self],
        *args,
        **kwargs,
    ) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance


    @inject
    def __init__(
        self,
        request: Request,
        database: Database,
        table: Table,
    ) -> None:
        super().__init__(
            request  = request,
            database = database,
            table    = table,
        )


    def run(
        self,
    ) -> bool:
        request_factory = self.request
        table = self.table

        if not request_factory:
            raise Exception("no table. to-do later")

        if not table:
            raise Exception("no table. to-do later")

        fetched:   bool = False
        next_href: str  = str()

        while not fetched:
            if next_href:
                request: Request = request_factory(url = next_href)
            else:
                request: Request = request_factory()

            response: Response = request.send()
            result: dict[str, Any] = response.json()

            collection: list[dict[str, Any]] = result[ResponseKeysEnum.COLLECTION]
            next_href = result[ResponseKeysEnum.NEXT_HREF]

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
