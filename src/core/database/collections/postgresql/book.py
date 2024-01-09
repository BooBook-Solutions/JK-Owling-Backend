from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import declarative_base

from core.database.collections.postgresql.common import BasePostgresCollection
from core.schemas import Book

Base = declarative_base()


class PostgresBook(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    author = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    cover = Column(String, nullable=True)
    quantity = Column(Integer, nullable=True)


class BookCollection(BasePostgresCollection[Book]):

    def __init__(self, session, engine):
        super().__init__(session)
        Base.metadata.create_all(bind=engine)
        self.session = session
        self.instance_class = Book
        self.postgres_class = PostgresBook
