from typing import Optional

from pydantic import BaseModel


class ProjectMemberCreateSchema(BaseModel):
    user_id: int
    discipline: str


class ProjectMemberApprovalSchema(BaseModel):
    approved: bool
    approval_note: Optional[str] = None


class ProjectMemberSchema(BaseModel):
    id: int
    project_id: int
    user_id: int
    discipline: str
    approved: bool
    approval_note: Optional[str] = None
    user_name: Optional[str] = None
    user_specialty: Optional[str] = None
    user_image_url: Optional[str] = None
