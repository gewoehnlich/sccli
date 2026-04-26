from datetime import datetime
from typing import Any
from loguru import logger


class Logger:
    def __init__(
        self,
    ) -> None:
        date: str = datetime.today().strftime('%Y-%m-%d')

        logger.add(f"logs/{date}.log")

        self.__logger = logger

    def __getattr__(
        self,
        name: str,
    ) -> Any:
        return getattr(self.__logger, name)
