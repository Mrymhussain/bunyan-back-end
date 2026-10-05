from typing import Optional

from pydantic import BaseModel, ConfigDict


class ServiceCategoryCreateSchema(BaseModel):
    name: str


class ServiceCategoryUpdateSchema(BaseModel):
    name: Optional[str] = None


class ServiceCategorySchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)