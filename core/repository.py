from abc import abstractmethod
from typing import Protocol
from core.dto import Dto


class Repository(
    Protocol
):
    @abstractmethod
    def get(
        self,
        dto: Dto,
    ) -> Dto:
        ...


    @abstractmethod
    def create(
        self,
        dto: Dto,
    ) -> Dto:
        ...


    @abstractmethod
    def update(
        self,
        dto: Dto,
    ) -> Dto:
        ...


    @abstractmethod
    def delete(
        self,
        dto: Dto,
    ) -> Dto:
        ...
