from typing import Self
from pydantic import BaseModel
from urllib.parse import urlencode
from enums.url_enum import UrlEnum


class UrlGenerator(
    BaseModel
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


    @classmethod
    def auth_url(
        cls,
        client_id:      str,
        redirect_uri:   str,
        code_challenge: str,
        state:          str,
    ) -> str:
        params: dict[str, str] = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "state": state,
        }

        link: str = UrlEnum.AUTH

        return f"{link}?{urlencode(query = params)}"
