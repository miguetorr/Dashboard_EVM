"""Repositorio base abstracto."""

from abc import ABC, abstractmethod
from typing import TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

T = TypeVar("T")


class AbstractRepository(ABC):
    """Contrato que deben cumplir todos los repositorios."""

    def __init__(self, db: Session) -> None:
        self.db = db

    @abstractmethod
    def get_all(self) -> list[T]:
        ...

    @abstractmethod
    def get_by_id(self, entity_id: UUID) -> T | None:
        ...

    @abstractmethod
    def create(self, entity: T) -> T:
        ...

    @abstractmethod
    def update(self, entity: T, data: dict) -> T:
        ...

    @abstractmethod
    def delete(self, entity: T) -> None:
        ...
