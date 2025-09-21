import json

from core.dto import Dto
from core.resource import Resource


class JsonResource(
    Resource
):
    def from_dto(
        self,
        dto: Dto,
    ) -> str:
