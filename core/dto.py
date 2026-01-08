import json
from typing import Any, Self
from pydantic import BaseModel


class Dto(
    BaseModel
):
    pass
    # def from_file(
    #     self,
    #     file: str,
    # ) -> Self:
    #     return self
    #
    # def from_dict(
    #     self,
    #     data: dict[str, Any],
    # ) -> Self:
    #     return self
    #
    # def validate_kind(
    #     self,
    #     actual_kind: str,
    #     expected_kind: str,
    # ) -> bool:
    #     if actual_kind != expected_kind:
    #         raise Exception("to-do message wrong kind")
    #
    #     return True
