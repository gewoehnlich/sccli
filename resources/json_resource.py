import json
from typing import Any

from core.dto import Dto
from core.resource import Resource


class JsonResource(
    Resource
):
    def from_dto(
        self,
        dto: Dto,
    ) -> str:
        model_dict: dict[str, Any] = dto.model_dump()

        return json.dumps(
            obj = model_dict,
            indent = 4,
        )
