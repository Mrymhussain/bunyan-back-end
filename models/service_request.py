from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from .base import BaseModel


class ServiceRequestModel(BaseModel):
    __tablename__ = "service_requests"

    client_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    specialist_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    service_category_id = Column(
        Integer,
        ForeignKey("service_categories.id"),
        nullable=False
    )

    description = Column(Text, nullable=False)
    location = Column(String, nullable=False)
    preferred_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default="pending")