from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProjectCreateSchema(BaseModel):
    title: str
    project_type: str
    description: Optional[str] = None
    location: str
    budget_range: Optional[str] = None


class ProjectUpdateSchema(BaseModel):
    title: Optional[str] = None
    project_type: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    budget_range: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[int] = None


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

    model_config = ConfigDict(from_attributes=True)