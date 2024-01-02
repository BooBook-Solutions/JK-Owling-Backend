from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.authentication import authenticated_user, authenticated_admin
from app.common import RequestException
from app.database import get_db
import logging

from core.schemas import Order

logger = logging.getLogger("app.routers.order")

router = APIRouter(
    tags=["order"]
)


@router.get("", response_model=List[Order])
async def get_orders(user_id: str = None, db=Depends(get_db)):
    orders = await db.get_collection("order").filter(user_id)
    return orders


@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str, db=Depends(get_db)):
    order = await db.get_collection("order").get(order_id)
    return order


@router.post("", response_model=Order)
async def create_order(order: Order, user=Depends(authenticated_user), db=Depends(get_db)):
    order = await db.get_collection("order").create(order)
    logger.info("Admin " + str(user.id) + " created order: " + str(order))
    return order


@router.put("/{order_id}", response_model=Order)
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
    return order


@router.delete("/{order_id}", response_model=Order)
async def delete_order(order_id: str, user=Depends(authenticated_user), db=Depends(get_db)):
    order = await db.get_collection("order").get(order_id)
    if order is None:
        raise RequestException("Order not found")
    if order.user_id != user.id:
        raise RequestException("You are not allowed to delete this order")
    result = await db.get_collection("order").delete(order_id)
    if result:
        logger.info("User " + str(user.id) + " deleted order: " + str(order))
    else:
        raise RequestException("Could not delete order")
    return order

