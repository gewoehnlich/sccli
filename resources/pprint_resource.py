from pprint import pprint
from typing import Any

from core.resource import Resource


class PprintResource(Resource):
    def print(
        self,
        data: Any,
    ) -> None:
        pprint(data)
