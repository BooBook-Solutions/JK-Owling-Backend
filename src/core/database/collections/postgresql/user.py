from typing import List, Optional

from sqlalchemy import Column, String, Enum, Integer
from sqlalchemy.orm import declarative_base

from core.database.collections.postgresql.common import BasePostgresCollection
from core.schemas.user import User
from app.settings import ADMIN_ROLE, USER_ROLE

Base = declarative_base()


class PostgresUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True)
    picture = Column(String, nullable=True)
    role = Column(Enum(ADMIN_ROLE, USER_ROLE, name='user_role'), nullable=True)


class UserCollection(BasePostgresCollection[User]):

    def __init__(self, session, engine):
        super().__init__(session)
        Base.metadata.create_all(bind=engine)
        self.session = session
        self.instance_class = User
        self.postgres_class = PostgresUser

    async def get(self, email: Optional[str], **kwargs) -> User:
        user_id = kwargs.get("user_id")
        if user_id:
            item = self.session.query(self.postgres_class).filter(self.postgres_class.id == user_id).first()
            return self.to_pydantic(item, self.instance_class)
        item = self.session.query(self.postgres_class).filter(self.postgres_class.email == email).first()
        return self.to_pydantic(item, self.instance_class)
