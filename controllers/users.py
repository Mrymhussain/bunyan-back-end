from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.user import UserModel
from serializers.user import UserSchema, UserUpdateSchema

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
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int,
    data: UserUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if data.email and data.email != user.email:
        existing_user = (
            db.query(UserModel)
            .filter(UserModel.email == data.email)
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    db.delete(current_user)
    db.commit()