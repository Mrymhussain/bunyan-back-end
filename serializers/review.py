from typing import Optional

from pydantic import BaseModel, ConfigDict


class ReviewCreateSchema(BaseModel):
    reviewed_user_id: int
    rating: int
    comment: Optional[str] = None


class ReviewUpdateSchema(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None


class ReviewSchema(BaseModel):
    id: int
    client_id: int
    reviewed_user_id: int
    rating: int
    comment: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)