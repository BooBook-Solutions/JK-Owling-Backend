from core.database.collections.mongodb.common import BaseMongoCollection
from core.schemas import Book


class BookCollection(BaseMongoCollection[Book]):

    def __init__(self, database):
        super().__init__(database)
        self.collection = database.book
        self.instance_class = Book
