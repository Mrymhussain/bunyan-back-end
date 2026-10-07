from datetime import datetime

from pydantic import BaseModel


class ProjectUpdateCreateSchema(BaseModel):
    message: str


class ProjectUpdateSchema(BaseModel):
    id: int
    project_id: int
    author_id: int
    author_name: str
    author_role: str
    message: str
    created_at: datetime
