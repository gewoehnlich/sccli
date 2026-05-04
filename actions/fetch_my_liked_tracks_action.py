from pprint import pprint
import sys
from time import sleep
from typing import Any

from rich import inspect

from core.action import Action
from core.auth import Auth
from core.request import Request
from models.user import User
from repositories.track_repository import TrackRepository
from repositories.user_repository import UserRepository


class FetchMyLikedTracksAction(Action):
    def __init__(
        self,
        auth: Auth,
        request: type[Request],
        track_repository: TrackRepository,
        user_repository: UserRepository,
    ) -> None:
        super().__init__(
            auth=auth,
            request=request,
        )

        self.track_repository = track_repository
        self.user_repository = user_repository

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
                for track in collection:
                    user: User = self.user_repository.store(
                        avatar_url=track["user"]["avatar_url"],
                        city=track["user"]["city"],
                        country=track["user"]["country"],
                        created_at=track["user"]["created_at"],
                        description=track["user"]["description"],
                        id=track["user"]["id"],
                        permalink=track["user"]["permalink"],
                        permalink_url=track["user"]["permalink_url"],
                        username=track["user"]["username"],
                    )

                    self.track_repository.store(
                        artwork_url=track["artwork_url"],
                        created_at=track["created_at"],
                        description=track["description"],
                        duration=track["duration"],
                        id=track["id"],
                        permalink_url=track["permalink_url"],
                        title=track["title"],
                        user_id=user.id,
                    )

            if not next_href:
                fetched = True

            sleep(5)

        # to-do: catch Exceptions

        return True
