import json
from typing import Any, Self
from pydantic import BaseModel


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

    def from_dict(
        self,
        data: dict[str, Any],
    ) -> Self:
        pass

    def validate_kind(
        self,
        actual_kind: str,
        expected_kind: str,
    ) -> bool:
        if actual_kind != expected_kind:
            raise Exception("to-do message wrong kind")

        return True
