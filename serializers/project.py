from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProjectCreateSchema(BaseModel):
    title: str
    project_type: str
    description: Optional[str] = None
    location: str
    budget_range: Optional[str] = None
    image_url: Optional[str] = None


class ProjectUpdateSchema(BaseModel):
    title: Optional[str] = None
    project_type: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    budget_range: Optional[str] = None
    image_url: Optional[str] = None


class ProjectWorkUpdateSchema(BaseModel):
    status: Optional[str] = None
    progress: Optional[int] = None


class ProjectMeetingSchema(BaseModel):
    meeting_title: Optional[str] = None
    meeting_at: Optional[datetime] = None
    meeting_type: Optional[str] = None
    meeting_link: Optional[str] = None


class ProjectSchema(BaseModel):
    id: int
    client_id: int
    title: str
    project_type: str
    description: Optional[str] = None
    location: str
    budget_range: Optional[str] = None
    status: str
    progress: int
    image_url: Optional[str] = None
    meeting_title: Optional[str] = None
    meeting_at: Optional[datetime] = None
    meeting_type: Optional[str] = None
    meeting_link: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
