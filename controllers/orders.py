from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.order import OrderModel
from models.user import UserModel
from serializers.order import (
    OrderCreateSchema,
    OrderSchema,
    OrderUpdateSchema,
)

router = APIRouter(prefix="/orders")


def get_order_or_404(order_id, db):
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

    return order


@router.post("", response_model=OrderSchema, status_code=201)
def create_order(
    data: OrderCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != "client":
        raise HTTPException(
            status_code=403,
            detail="Only clients can create orders"
        )

    supplier = (
        db.query(UserModel)
        .filter(UserModel.id == data.supplier_id)
        .first()
    )

    if not supplier:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found"
        )

    if supplier.role != "supplier":
        raise HTTPException(
            status_code=400,
            detail="Selected user is not a supplier"
        )

    order = OrderModel(
        client_id=current_user.id,
        supplier_id=data.supplier_id,
        total_price=0,
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


@router.get("", response_model=list[OrderSchema])
def get_orders(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role == "admin":
        return db.query(OrderModel).all()

    return (
        db.query(OrderModel)
        .filter(
            or_(
                OrderModel.client_id == current_user.id,
                OrderModel.supplier_id == current_user.id,
            )
        )
        .all()
    )


@router.get("/{order_id}", response_model=OrderSchema)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    order = get_order_or_404(order_id, db)

    allowed = (
        current_user.role == "admin"
        or order.client_id == current_user.id
        or order.supplier_id == current_user.id
    )

    if not allowed:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return order


@router.put("/{order_id}", response_model=OrderSchema)
def update_order(
    order_id: int,
    data: OrderUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    order = get_order_or_404(order_id, db)

    if (
        current_user.role != "supplier"
        or order.supplier_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Only the assigned supplier can update order status"
        )

    update_data = data.model_dump(exclude_unset=True)

    status = update_data.get("status")

    if status is None:
        raise HTTPException(
            status_code=400,
            detail="Supplier can only update order status"
        )

    allowed_statuses = [
        "pending",
        "processing",
        "ready",
        "completed",
    ]

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid order status"
        )

    order.status = status

    db.commit()
    db.refresh(order)

    return order


@router.delete("/{order_id}", status_code=204)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    order = get_order_or_404(order_id, db)

    if order.client_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the client can cancel this order"
        )

    if order.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Only pending orders can be cancelled"
        )

    db.delete(order)
    db.commit()
