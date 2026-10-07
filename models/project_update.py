from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import BaseModel


class ProjectUpdateModel(BaseModel):
    __tablename__ = "project_updates"

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    author_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )
