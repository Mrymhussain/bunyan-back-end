from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import UserModel
from serializers.user import UserSchema

router = APIRouter(prefix="/users")


@router.get("", response_model=list[UserSchema])
def get_users(
    role: Optional[str] = None,
    specialty: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(UserModel)

    if role:
        query = query.filter(UserModel.role == role)

    if specialty:
        query = query.filter(UserModel.specialty == specialty)

    return query.all()


@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user