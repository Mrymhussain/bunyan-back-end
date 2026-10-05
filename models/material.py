from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text

from .base import BaseModel


class MaterialModel(BaseModel):
    __tablename__ = "materials"

    supplier_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)