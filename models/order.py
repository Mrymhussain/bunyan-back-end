from sqlalchemy import Column, Float, ForeignKey, Integer, String

from .base import BaseModel


class OrderModel(BaseModel):
    __tablename__ = "orders"

    client_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    supplier_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    total_price = Column(
        Float,
        nullable=False,
        default=0
    )

    status = Column(
        String,
        nullable=False,
        default="pending"
    )