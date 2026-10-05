from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.material import MaterialModel
from models.order import OrderModel
from models.order_item import OrderItemModel
from models.user import UserModel
from serializers.order_item import (
    OrderItemCreateSchema,
    OrderItemSchema,
)

router = APIRouter(prefix="/orders")


@router.get(
    "/{order_id}/items",
    response_model=list[OrderItemSchema]
)
def get_order_items(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    order = (
        db.query(OrderModel)
        .filter(OrderModel.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if (
        order.client_id != current_user.id
        and order.supplier_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return (
        db.query(OrderItemModel)
        .filter(OrderItemModel.order_id == order_id)
        .all()
    )


@router.post(
    "/{order_id}/items",
    response_model=OrderItemSchema,
    status_code=201
)
def add_order_item(
    order_id: int,
    data: OrderItemCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    order = (
        db.query(OrderModel)
        .filter(OrderModel.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.client_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    if data.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    material = (
        db.query(MaterialModel)
        .filter(MaterialModel.id == data.material_id)
        .first()
    )

    if not material:
        raise HTTPException(
            status_code=404,
            detail="Material not found"
        )

    if material.supplier_id != order.supplier_id:
        raise HTTPException(
            status_code=400,
            detail="Material does not belong to this supplier"
        )

    item = OrderItemModel(
        order_id=order_id,
        material_id=data.material_id,
        quantity=data.quantity,
        unit_price=material.price,
    )

    order.total_price += material.price * data.quantity

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@router.delete(
    "/{order_id}/items/{item_id}",
    status_code=204
)
def delete_order_item(
    order_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    order = (
        db.query(OrderModel)
        .filter(OrderModel.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.client_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    item = (
        db.query(OrderItemModel)
        .filter(
            OrderItemModel.id == item_id,
            OrderItemModel.order_id == order_id,
        )
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Order item not found"
        )

    order.total_price -= item.unit_price * item.quantity

    if order.total_price < 0:
        order.total_price = 0

    db.delete(item)
    db.commit()