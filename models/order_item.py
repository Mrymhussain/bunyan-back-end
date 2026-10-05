from sqlalchemy import Column, Float, ForeignKey, Integer

from .base import BaseModel


class OrderItemModel(BaseModel):
    __tablename__ = "order_items"

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    material_id = Column(
        Integer,
        ForeignKey("materials.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    unit_price = Column(
        Float,
        nullable=False
    )