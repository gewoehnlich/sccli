import json
from time import time
from typing import Self
from core.dto import Dto


class TokensDto(Dto):
    def fromJsonFile(
        self,
        json_file: str,
    ) -> Self:
        with open(
            file = json_file,
            mode = "r",
            encoding = "utf-8",
        ) as file:
            data: dict[str, str] = json.loads(
                file.read().strip()
            )

            self.access_token:  str = data["access_token"]
            self.token_type:    str = data["token_type"]
            self.expires_in:    str = data["expires_in"]
            self.refresh_token: str = data["refresh_token"]
            self.timestamp:     str = data["timestamp"]            

            self.current_timestamp: int = int(time())
            self.expire_timestamp:  int = (
                int(self.timestamp) + int(self.expires_in)
            )

            return self
