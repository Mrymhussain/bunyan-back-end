from pydantic import BaseModel, ConfigDict


class ProjectMemberCreateSchema(BaseModel):
    user_id: int
    discipline: str


class ProjectMemberSchema(BaseModel):
    id: int
    project_id: int
    user_id: int
    discipline: str

    model_config = ConfigDict(from_attributes=True)