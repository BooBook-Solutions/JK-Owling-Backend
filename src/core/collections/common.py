from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseCollection(ABC, Generic[T]):

    def __init__(self, database):
        self.collection = database.user

    @abstractmethod
    def get(self, **kwargs) -> T:
        pass

    @abstractmethod
    def create(self, **kwargs) -> T:
        pass

    @abstractmethod
    def update(self, **kwargs) -> T:
        pass

    @abstractmethod
    def delete(self, **kwargs) -> T:
        pass

    @abstractmethod
    def filter(self, **kwargs) -> List[T]:
        pass
