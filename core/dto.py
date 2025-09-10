import json
from typing import Self


class Dto:
    def fromFile(
        self,
        filepath: str
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

