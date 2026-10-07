from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.review import ReviewModel
from models.user import UserModel
from serializers.review import (
    ReviewCreateSchema,
    ReviewSchema,
)

router = APIRouter(prefix="/reviews")


@router.post("", response_model=ReviewSchema, status_code=201)
def create_review(
    data: ReviewCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != "client":
        raise HTTPException(
            status_code=403,
            detail="Only clients can create reviews"
        )

    reviewed_user = (
        db.query(UserModel)
        .filter(UserModel.id == data.reviewed_user_id)
        .first()
    )

    if not reviewed_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if reviewed_user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot review yourself"
        )

    if data.rating < 1 or data.rating > 5:
        raise HTTPException(
            status_code=400,
            detail="Rating must be between 1 and 5"
        )

    review = ReviewModel(
        client_id=current_user.id,
        reviewed_user_id=data.reviewed_user_id,
        rating=data.rating,
        comment=data.comment,
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review


@router.get("", response_model=list[ReviewSchema])
def get_reviews(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role == "admin":
        return db.query(ReviewModel).all()

    if current_user.role == "client":
        return (
            db.query(ReviewModel)
            .filter(ReviewModel.client_id == current_user.id)
            .all()
        )

    return (
        db.query(ReviewModel)
        .filter(
            ReviewModel.reviewed_user_id == current_user.id
        )
        .all()
    )


@router.get("/{review_id}", response_model=ReviewSchema)
def get_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    review = (
        db.query(ReviewModel)
        .filter(ReviewModel.id == review_id)
        .first()
    )

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    if current_user.role == "admin":
        return review

    if (
        current_user.role == "client"
        and review.client_id == current_user.id
    ):
        return review

    if review.reviewed_user_id == current_user.id:
        return review

    raise HTTPException(
        status_code=403,
        detail="Not authorized"
    )


@router.delete("/{review_id}", status_code=204)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admins can delete reviews"
        )

    review = (
        db.query(ReviewModel)
        .filter(ReviewModel.id == review_id)
        .first()
    )

    if not review:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    db.delete(review)
    db.commit()
