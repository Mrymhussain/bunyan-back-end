from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderCreateSchema(BaseModel):
    supplier_id: int
    total_price: float


class OrderUpdateSchema(BaseModel):
    status: Optional[str] = None
    total_price: Optional[float] = None


class OrderSchema(BaseModel):
    id: int
    client_id: int
    supplier_id: int
    total_price: float
    status: str

    model_config = ConfigDict(from_attributes=True)