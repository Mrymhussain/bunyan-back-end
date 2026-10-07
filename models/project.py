from sqlalchemy import Column, ForeignKey, Integer, String, Text

from .base import BaseModel


class ProjectModel(BaseModel):
    __tablename__ = "projects"

    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    project_type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=False)
    budget_range = Column(String, nullable=True)
    status = Column(String, nullable=False, default="pending")
    progress = Column(Integer, nullable=False, default=0)
    image_url = Column(String, nullable=True)
