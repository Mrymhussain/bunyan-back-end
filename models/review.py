from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import BaseModel


class ReviewModel(BaseModel):
    __tablename__ = "reviews"

    client_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    reviewed_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    rating = Column(
        Integer,
        nullable=False
    )

    comment = Column(
        Text,
        nullable=True
    )