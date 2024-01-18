from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.authentication import authenticated_user, authenticated_admin
from app.common import RequestException
from app.database import get_db
import logging

from app.settings import ADMIN_ROLE
from core.schemas import Order
from core.schemas.order import OrderPost, Status, OrderGetResponse, StatusGetResponse, StatusMapping

logger = logging.getLogger("app.routers.order")

router = APIRouter(
    tags=["order"]
)


@router.get("/status", response_model=List[StatusGetResponse])
async def get_statuses():
    statuses = list(Status)
    response = [StatusGetResponse(name=status, name_translated=StatusMapping.from_status(status))
                for status in statuses]
    return response


@router.get("", response_model=List[OrderGetResponse])
async def get_orders(user_id: str = None, db=Depends(get_db), user=Depends(authenticated_user)):
    if user.role != ADMIN_ROLE:
        if user_id is not None and str(user.id) != user_id:
            raise RequestException("You are not allowed to get the orders of this user")
        user_id = str(user.id)
    orders = await db.get_collection("order").filter(user_id)
    orders_response = []
    for order in orders:
        order_response = await return_order(order, db)
        orders_response.append(order_response)
    return orders_response


@router.get("/{order_id}", response_model=OrderGetResponse)
async def get_order(order_id: str, db=Depends(get_db), user=Depends(authenticated_user)):
    order = await db.get_collection("order").get(order_id)
    if order is None:
        raise RequestException("Order not found")
    if user.role != ADMIN_ROLE and order.user != user.id:
        raise RequestException("You are not allowed to get this order")

    return await return_order(order, db)


@router.post("", response_model=OrderGetResponse)
async def create_order(order: OrderPost, user=Depends(authenticated_user), db=Depends(get_db)):
    order = Order(**{
        "user": order.user_id,
        "book": order.book_id,
        "quantity": order.quantity,
        "status": Status.PENDING
    })
    if user.role != ADMIN_ROLE and order.user != user.id:
        raise RequestException("You are not allowed to create an order for this user")

    book = await db.get_collection("book").get(order.book)
    if book is None:
        raise RequestException("Book not found")
    request_user = await db.get_collection("user").get(None, user_id=order.user)
    if request_user is None:
        raise RequestException("User not found")
    if book.quantity < order.quantity:
        raise RequestException("Not enough books in stock")
    book = book.model_copy(update={"quantity": book.quantity - order.quantity})
    book = await db.get_collection("book").update(book)

    order = await db.get_collection("order").create(order)
    logger.info("Admin " + str(user.id) + " created order: " + str(order))

    return await return_order(order, db)


@router.put("/{order_id}", response_model=OrderGetResponse)
async def update_order(order_id: str, request: Request, user=Depends(authenticated_admin), db=Depends(get_db)):
    order = await db.get_collection("order").get(order_id)
    if order is None:
        raise RequestException("Order not found")

    data = await request.json()
    status = data.get("status")
    if status is None:
        raise RequestException("No status provided")
    order = await db.get_collection("order").update(order_id, status=status)

    logger.info("Admin " + str(user.id) + " updated order: " + str(order))

    return await return_order(order, db)


@router.delete("/{order_id}", response_model=OrderGetResponse)
async def delete_order(order_id: str, user=Depends(authenticated_user), db=Depends(get_db)):
    order = await db.get_collection("order").get(order_id)
    if order is None:
        raise RequestException("Order not found")
    order_user = await db.get_collection("user").get(None, user_id=order.user)
    if user.role != ADMIN_ROLE and order_user and order.user != user.id:
        raise RequestException("You are not allowed to delete this order")

    if user.role != ADMIN_ROLE and order.status != Status.PENDING:
        raise RequestException("You are not allowed to delete a non pending order")

    result = await db.get_collection("order").delete(order_id)
    if result:
        logger.info("User " + str(user.id) + " deleted order: " + str(order))
    else:
        raise RequestException("Could not delete order")

    # restore book quantity
    book = await db.get_collection("book").get(order.book)
    book = book.model_copy(update={"quantity": book.quantity + order.quantity})
    book = await db.get_collection("book").update(book)

    return await return_order(order, db)


async def return_order(order: Order, db) -> OrderGetResponse:
    user = await db.get_collection("user").get(None, user_id=order.user)
    book = await db.get_collection("book").get(order.book)
    return OrderGetResponse(**{
        "id": order.id,
        "user": user,
        "book": book,
        "quantity": order.quantity,
        "status": StatusGetResponse(name=order.status, name_translated=StatusMapping.from_status(order.status))
    })
