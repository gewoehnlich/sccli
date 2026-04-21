from typing import Any
from time import sleep
from pprint import pprint
from rich import inspect

from core.auth import Auth
from core.action import Action
from core.request import Request
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
        request_factory = self.request
        inspect(request_factory)

        if not request_factory:
            raise Exception("no table. to-do later")

        fetched: bool = False
        next_href: str = str()

        while not fetched:
            if next_href:
                request: Request = request_factory(
                    access_token=self.auth.get_access_token(),
                    url=next_href,
                )
            else:
                request: Request = request_factory(
                    access_token=self.auth.get_access_token(),
                )

            response: dict[str, dict[str, str | int] | str] = request.send()

            collection: list[dict[str, Any]] = response["collection"]
            next_href = response["next_href"]

            if collection:
                pprint(collection)
                for track in collection:
                    self.repository.create(
                        access=track["access"],
                        artwork_url=track["artwork_url"],
                        comment_count=track["comment_count"],
                        created_at=track["created_at"],
                        description=track["description"],
                        duration=track["duration"],
                        favoritings_count=track["favoritings_count"],
                        id=track["id"],
                        metadata_artist=track["metadata_artist"],
                        permalink_url=track["permalink_url"],
                        playback_count=track["playback_count"],
                        reposts_count=track["reposts_count"],
                        stream_url=track["stream_url"],
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
