from typing import List, Optional

from sqlalchemy import Column, String, Enum, Integer
from sqlalchemy.orm import declarative_base

from core.database.collections.postgresql.common import BasePostgresCollection
from core.schemas.order import Status, Order

Base = declarative_base()


class PostgresOrder(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user = Column(String, nullable=True)
    book = Column(String, nullable=True)
    quantity = Column(Integer, nullable=True)
    status = Column(Enum(Status.PENDING.value, Status.APPROVED.value, Status.REJECTED.value,
                         name='order_status'), nullable=True)


class OrderCollection(BasePostgresCollection[Order]):

    def __init__(self, session, engine):
        super().__init__(session)
        Base.metadata.create_all(bind=engine)
        self.session = session
        self.instance_class = Order
        self.postgres_class = PostgresOrder

    async def filter(self, user_id: Optional[str] = None, book_id: Optional[str] = None, **kwargs) -> List[Order]:
        if user_id is None:
            if book_id is None:
                items = self.session.query(self.postgres_class).all()
            else:
                items = self.session.query(self.postgres_class).filter_by(book=book_id).all()
        elif book_id is None:
            items = self.session.query(self.postgres_class).filter_by(user=user_id).all()
        else:
            items = self.session.query(self.postgres_class).filter_by(user=user_id, book=book_id).all()
        return self.to_pydantic(items, List[Order])

    async def update(self, order_id: str, **kwargs) -> Order:
        status = kwargs.get('status')
        self.session.query(self.postgres_class).filter_by(id=order_id).update({"status": status})
        self.session.commit()
        item = self.session.query(self.postgres_class).filter_by(id=order_id).first()
        return self.to_pydantic(item, Order)
