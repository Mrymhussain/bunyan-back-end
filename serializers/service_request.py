from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ServiceRequestCreateSchema(BaseModel):
    specialist_id: int
    service_category_id: int
    description: str
    location: str
    preferred_date: datetime


class ServiceRequestUpdateSchema(BaseModel):
    specialist_id: Optional[int] = None
    service_category_id: Optional[int] = None
    description: Optional[str] = None
    location: Optional[str] = None
    preferred_date: Optional[datetime] = None
    status: Optional[str] = None


class ServiceRequestSchema(BaseModel):
    id: int
    client_id: int
    specialist_id: int
    service_category_id: int
    description: str
    location: str
    preferred_date: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)