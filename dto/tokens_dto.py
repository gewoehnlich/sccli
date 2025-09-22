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


    def __init__(
        self,
    ) -> None:
        super().__init__()


    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> Self:
        data_copy = data.copy()
        data_copy["expires_in"] = int(data_copy["expires_in"])

        instance = cls(**data_copy)
        instance.timestamp = int(time())

        return instance


    @classmethod
    def from_json(
        cls,
        json_string: str,
    ) -> Self:
        data: dict[str, str] = json.loads(
            s = json_string,
        )

        return cls.from_dict(data)


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

            instance = cls.from_dict(data)
            instance.timestamp = int(data["timestamp"])
            instance.current_timestamp = int(time())
            instance.expire_timestamp = instance.timestamp + instance.expires_in

            return instance
