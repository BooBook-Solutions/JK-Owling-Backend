from typing import List, Optional

from bson import ObjectId

from core.collections.common import BaseCollection
from core.schemas import Book


class BookCollection(BaseCollection[Book]):

    def __init__(self, database):
        super().__init__(database)
        self.collection = database.book

    async def get(self, book_id: str) -> Book:
        print(book_id)
        book = await self.collection.find_one({"_id": ObjectId(book_id)})
        return self.to_pydantic(book, Book)

    async def filter(self, name: Optional[str] = None) -> List[Book]:
        books = await self.collection.find().to_list(length=None)
        return self.to_pydantic(books, List[Book])

    async def create(self) -> Book:
        pass

    async def update(self) -> Book:
        pass

    async def delete(self) -> Book:
        pass
