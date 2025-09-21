import json
from time import time
from typing import Any, Self
from core.dto import Dto


class TokensDto(
    Dto
):
    access_token:  str
    token_type:    str
    expires_in:    int
    refresh_token: str

    timestamp:         int | None
    current_timestamp: int | None
    expire_timestamp:  int | None


    def __init__(
        self,
    ) -> None:
        super().__init__()


    def from_dict(
        self,
        data: dict[str, Any],
    ) -> Self:
        # make it static? so the cls would be passed instead of self

        self.access_token  = data["access_token"]
        self.token_type    = data["token_type"]
        self.expires_in    = int(data["expires_in"])
        self.refresh_token = data["refresh_token"]
        self.timestamp     = int(time())

        return self


    def from_json(
        self,
        json_string: str,
    ) -> Self:
        data: dict[str, str] = json.loads(
            s = json_string,
        )

        self.access_token  = data["access_token"]
        self.token_type    = data["token_type"]
        self.expires_in    = int(data["expires_in"])
        self.refresh_token = data["refresh_token"]

        return self


    def from_file(
        self,
        file: str,
    ) -> Self:
        with open(
            file = file,
            mode = "r",
            encoding = "utf-8",
        ) as f:
            # add fileformat checking
            data: dict[str, str] = json.loads(
                f.read().strip()
            )

            self.access_token  = data["access_token"]
            self.token_type    = data["token_type"]
            self.expires_in    = int(data["expires_in"])
            self.refresh_token = data["refresh_token"]
            self.timestamp     = int(data["timestamp"])

            self.current_timestamp = int(time())
            self.expire_timestamp  = self.timestamp + self.expires_in

            return self
