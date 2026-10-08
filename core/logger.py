from pathlib import Path

from loguru import logger


class Logger:
    def __init__(
        self,
        directory: Path,
        level: str = "INFO",
    ) -> None:
        self._handler_id: int = logger.add(
            directory / "{time:YYYY-MM-DD}.log",  # date taken at file creation
            level=level,
            rotation="00:00",  # new file at midnight
            retention="14 days",
            encoding="utf-8",
            enqueue=True,
            backtrace=True,
            diagnose=False,  # never dump variable values (secrets) into logs
        )

    def close(self) -> None:
        logger.remove(self._handler_id)

    def debug(self, message: str, *args: object, **kwargs: object) -> None:
        logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args: object, **kwargs: object) -> None:
        logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args: object, **kwargs: object) -> None:
        logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args: object, **kwargs: object) -> None:
        logger.error(message, *args, **kwargs)

    def exception(self, message: str, *args: object, **kwargs: object) -> None:
        logger.exception(message, *args, **kwargs)
