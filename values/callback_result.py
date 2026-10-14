from dataclasses import dataclass


@dataclass(frozen=True)
class CallbackResult:
    code: str | None
    state: str | None
    error: str | None
