from sqlalchemy import Column, String

from .base import BaseModel


class ServiceCategoryModel(BaseModel):
    __tablename__ = "service_categories"

    name = Column(String, unique=True, nullable=False)
    