from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

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

    approved = Column(
        Boolean,
        nullable=False,
        default=False
    )

    approval_note = Column(
        Text,
        nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "user_id",
            name="unique_project_member"
        ),
    )
