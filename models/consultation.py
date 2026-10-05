from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from .base import BaseModel


class ConsultationModel(BaseModel):
    __tablename__ = "consultations"

    client_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    engineer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    topic = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    scheduled_at = Column(DateTime, nullable=False)
    meeting_type = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")