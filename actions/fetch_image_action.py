from typing import Any

from core.action import Action
from core.auth import Auth
from core.http_client import HttpClient
from core.request import Request
from models.image import Image
from repositories.image_repository import ImageRepository


class FetchImageAction(Action):
    def __init__(
        self,
        auth: Auth,
        http_client: HttpClient,
        image_repository: ImageRepository,
    ) -> None:
        self.auth: Auth = auth
        self.http_client: HttpClient = http_client
        self.image_repository: ImageRepository = image_repository

    def run(self, url: str) -> bytes:
        cached = self.image_repository.get_one(
            primary_key=url,
        )

        if cached is not None:
            return cached.data

        request: Request = Request(
            method=Request.METHOD.GET,
            url=url,
            access_token=self.auth.get_access_token(),
            headers={
                "Content-Type": "image/jpeg",
            },
        )

        data = self.http_client.fetch_image(
            request=request,
        )

        self.image_repository.store(
            model=Image(url=url, data=data)
        )

        return data
