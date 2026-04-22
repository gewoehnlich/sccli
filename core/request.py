from typing import Any
from requests import Session, Request as BaseRequest
from rich import inspect


class Request:
    __session = Session()

    def __init__(
        self,
        method: str = "",
        url: str = "",
        headers: dict[str, str] = {
            "Accept": "application/json; charset=utf-8",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        params: dict[str, str] = {},
        data: dict[str, str] = {},
    ) -> None:
        self.__request = BaseRequest(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
        )

    def send(
        self,
    ) -> dict[str, Any]:
        response = self.__session.send(
            request=self.__request.prepare()
        )
        inspect(response)

        data: dict[str, Any] = response.json()

        return data
