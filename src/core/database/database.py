from abc import abstractmethod, ABC

from motor import motor_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import MONGODB_URL, POSTGRES_URL
from core.database.collections.mongodb import UserCollection as mongo_user, BookCollection as mongo_book, \
    OrderCollection as mongo_order
from core.database.collections.postgresql import UserCollection as postgres_user, BookCollection as postgres_book, \
    OrderCollection as postgres_order


class Database(ABC):

    def __init__(self):
        self.database = None
        self.collections = {}

    def get_collection(self, collection_name):
        return self.collections[collection_name]

    @abstractmethod
    def close(self):
        raise NotImplementedError


class MongoDatabase(Database):

    def __init__(self):
        super().__init__()
        self.client = motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
        self.database = self.client.melius
        self.collections = {
            "user": mongo_user(self.database),
            "book": mongo_book(self.database),
            "order": mongo_order(self.database)
        }

    def close(self):
        self.database.client.close()


class PostgresDatabase(Database):

    session_local = None

    def __init__(self):
        super().__init__()
        engine = create_engine(POSTGRES_URL)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        with self.session_local() as session:
            self.collections = {
                "user": postgres_user(session, engine),
                "book": postgres_book(session, engine),
                "order": postgres_order(session, engine)
            }

    def close(self):
        self.session_local.close_all()


def get_database(db_type: str) -> Database:
    if db_type == "mongodb":
        return MongoDatabase()
    elif db_type == "postgresql":
        return PostgresDatabase()
    else:
        raise ValueError("Database type is not supported")
