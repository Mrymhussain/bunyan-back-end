from typing import Optional

from pydantic import BaseModel, ConfigDict


class MaterialCreateSchema(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    price: float
    stock_quantity: int
    image_url: Optional[str] = None


class MaterialUpdateSchema(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    image_url: Optional[str] = None


class MaterialSchema(BaseModel):
    id: int
    supplier_id: int
    name: str
    category: str
    description: Optional[str] = None
    price: float
    stock_quantity: int
    image_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)