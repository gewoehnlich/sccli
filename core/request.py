from typing import Any

from requests import Request as BaseRequest, Session


class Request:
    __session = Session()

    def __init__(
        self,
        method: str = "",
        url: str = "",
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
        data: dict[str, str] | None = None,
    ) -> None:
        if data is None:
            data = {}
        if params is None:
            params = {}
        if headers is None:
            headers = {
                "Accept": "application/json; charset=utf-8",
                "Content-Type": "application/x-www-form-urlencoded",
            }
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
        response = self.__session.send(request=self.__request.prepare())

        data: dict[str, Any] = response.json()

        return data
