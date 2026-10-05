from pydantic import BaseModel, ConfigDict


class OrderItemCreateSchema(BaseModel):
    material_id: int
    quantity: int


class OrderItemSchema(BaseModel):
    id: int
    order_id: int
    material_id: int
    quantity: int
    unit_price: float

    model_config = ConfigDict(from_attributes=True)