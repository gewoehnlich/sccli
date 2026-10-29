from dataclasses import dataclass

from core.value import Value


@dataclass(frozen=True)
class CallbackResult(Value):
    code: str | None
    state: str | None
    error: str | None
