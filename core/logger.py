from pathlib import Path

from loguru import logger

from enums.logger_level import LoggerLevelEnum


class Logger:
    def __init__(
        self,
        directory: Path,
        level: LoggerLevelEnum,
    ) -> None:
        self._logger = logger.opt(depth=1)

        self._handler_id: int = self._logger.add(
            directory / "{time:YYYY-MM-DD}.log",
            level=level.value,
            rotation="00:00",
            retention="14 days",
            encoding="utf-8",
            enqueue=True,
            backtrace=True,
        )

    def close(self) -> None:
        self._logger.remove(self._handler_id)

        self._logger.complete()

    # https://loguru.readthedocs.io/en/stable/api/logger.html#levels

    def trace(self, message: str, *args: object, **kwargs: object) -> None:
        self._logger.trace(message, *args, **kwargs)

    def debug(self, message: str, *args: object, **kwargs: object) -> None:
        self._logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args: object, **kwargs: object) -> None:
        self._logger.info(message, *args, **kwargs)

    def success(self, message: str, *args: object, **kwargs: object) -> None:
        self._logger.success(message, *args, **kwargs)

    def warning(self, message: str, *args: object, **kwargs: object) -> None:
        self._logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args: object, **kwargs: object) -> None:
        self._logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args: object, **kwargs: object) -> None:
        self._logger.critical(message, *args, **kwargs)

    def exception(self, message: str, *args: object, **kwargs: object) -> None:
        self._logger.exception(message, *args, **kwargs)
