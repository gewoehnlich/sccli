from typing import Any
from time import sleep
from pprint import pprint
from rich import inspect

from api_requests.fetch_my_liked_tracks_request import FetchMyLikedTracksRequest
from core.auth import Auth
from core.action import Action
from core.request import Request
from enums.track_access import TrackAccessEnum
from repositories.track_repository import TrackRepository


class FetchMyLikedTracksAction(Action):
    def __init__(
        self,
        auth: Auth,
        request: type[Request],
        repository: TrackRepository,
    ) -> None:
        super().__init__(
            auth=auth,
            request=request,
            repository=repository,
        )

    def run(
        self,
    ) -> bool:
        fetched: bool = False
        next_href: str | None = None

        while not fetched:
            if next_href:
                request = self.request(
                    access_token=self.auth.get_access_token(),
                    url=next_href,
                )
            else:
                request = self.request(
                    access_token=self.auth.get_access_token(),
                )

            response: dict[str, Any] = request.send()

            collection: list[dict[str, Any]] = response["collection"]
            next_href = response["next_href"]

            if collection:
                pprint(collection)
                for track in collection:
                    self.repository.store(
                        access=track["access"],
                        artwork_url=track["artwork_url"],
                        created_at=track["created_at"],
                        description=track["description"],
                        duration=track["duration"],
                        id=track["id"],
                        permalink_url=track["permalink_url"],
                        title=track["title"],
                        uri=track["uri"],
                        urn=track["urn"],
                        user_favorite=track["user_favorite"],
                        user_playback_count=track["user_playback_count"],
                    )

            if not next_href:
                fetched = True

            sleep(5)

        # to-do: catch Exceptions

        return True
