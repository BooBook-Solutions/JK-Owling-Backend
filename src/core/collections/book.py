from typing import List

from core.collections.common import BaseCollection
from core.schemas import Book


class BookCollection(BaseCollection[Book]):

    def __init__(self, database):
        super().__init__(database)
        self.collection = database.book

    def get(self, book_id: int) -> Book:
        pass

    def filter(self) -> List[Book]:
        pass

    def create(self) -> Book:
        pass

    def update(self) -> Book:
        pass

    def delete(self) -> Book:
        pass
