from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ConsultationCreateSchema(BaseModel):
    engineer_id: int
    topic: str
    description: Optional[str] = None
    scheduled_at: datetime
    meeting_type: str


class ConsultationUpdateSchema(BaseModel):
    topic: Optional[str] = None
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    meeting_type: Optional[str] = None
    status: Optional[str] = None


class ConsultationSchema(BaseModel):
    id: int
    client_id: int
    engineer_id: int
    topic: str
    description: Optional[str] = None
    scheduled_at: datetime
    meeting_type: str
    status: str

    model_config = ConfigDict(from_attributes=True)