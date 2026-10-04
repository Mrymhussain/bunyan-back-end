from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint

from .base import BaseModel


class ProjectMemberModel(BaseModel):
    __tablename__ = "project_members"

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    discipline = Column(
        String,
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "user_id",
            name="unique_project_member"
        ),
    )