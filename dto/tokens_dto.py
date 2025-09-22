import json
from time import time
from typing import Any, Self
from core.dto import Dto


class TokensDto(
    Dto
):
    access_token:      str
    token_type:        str
    expires_in:        int
    refresh_token:     str
    timestamp:         int
    current_timestamp: int
    expire_timestamp:  int


    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> Self:
        return cls.__create(
            data = data,
        )


    @classmethod
    def from_json(
        cls,
        json_string: str,
    ) -> Self:
        data: dict[str, str] = json.loads(
            s = json_string,
        )

        return cls.__create(
            data = data,
        )


    @classmethod
    def from_file(
        cls,
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

            return cls.__create(
                data = data,
            )


    @classmethod
    def __create(
        cls,
        data: dict[str, Any],
    ) -> Self:
        access_token:      str = data["access_token"]
        token_type:        str = data["token_type"]
        expires_in:        int = int(data["expires_in"])
        refresh_token:     str = data["refresh_token"]
        timestamp:         int = data.get("timestamp", int(time()))
        current_timestamp: int = int(time())
        expire_timestamp:  int = current_timestamp + expires_in

        instance: Self = cls(
            access_token      = access_token,
            token_type        = token_type,
            expires_in        = expires_in,
            refresh_token     = refresh_token,
            timestamp         = timestamp,
            current_timestamp = current_timestamp,
            expire_timestamp  = expire_timestamp,
        )

        return instance
