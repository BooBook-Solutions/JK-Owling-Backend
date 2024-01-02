from core.collections.common import BaseCollection
from core.schemas import Book


class BookCollection(BaseCollection[Book]):

    def __init__(self, database):
        super().__init__(database)
        self.collection = database.book
        self.instance_class = Book
