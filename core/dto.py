import json
from typing import Self
from pydantic import BaseModel

from core.request import Request


class Dto(BaseModel):
    def from_file(
        self,
        filepath: str,
    ) -> Self:
        with open(
            file = filepath,
            mode = "r",
            encoding = "utf-8",
        ) as file:
            if filepath.endswith(".json"):
                data: dict[str, str] = json.loads(
                    file.read().strip()
                )

            return data

    def from_request(
        self,
        request: Request,
    ) -> Self:
        pass
