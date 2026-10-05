from typing import Optional

from pydantic import BaseModel, ConfigDict


class MaterialCreateSchema(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    price: float
    stock_quantity: int


class MaterialUpdateSchema(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None


class MaterialSchema(BaseModel):
    id: int
    supplier_id: int
    name: str
    category: str
    description: Optional[str] = None
    price: float
    stock_quantity: int

    model_config = ConfigDict(from_attributes=True)