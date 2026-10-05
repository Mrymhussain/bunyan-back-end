from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.service_category import ServiceCategoryModel
from models.user import UserModel
from serializers.service_category import (
    ServiceCategoryCreateSchema,
    ServiceCategorySchema,
    ServiceCategoryUpdateSchema,
)

router = APIRouter(prefix="/service-categories")


@router.get("", response_model=list[ServiceCategorySchema])
def get_service_categories(
    db: Session = Depends(get_db),
):
    return db.query(ServiceCategoryModel).all()


@router.post("", response_model=ServiceCategorySchema, status_code=201)
def create_service_category(
    data: ServiceCategoryCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admins can create service categories"
        )

    existing_category = (
        db.query(ServiceCategoryModel)
        .filter(ServiceCategoryModel.name == data.name)
        .first()
    )

    if existing_category:
        raise HTTPException(
            status_code=409,
            detail="Service category already exists"
        )

    category = ServiceCategoryModel(name=data.name)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.put("/{category_id}", response_model=ServiceCategorySchema)
def update_service_category(
    category_id: int,
    data: ServiceCategoryUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admins can update service categories"
        )

    category = (
        db.query(ServiceCategoryModel)
        .filter(ServiceCategoryModel.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Service category not found"
        )

    if data.name and data.name != category.name:
        existing_category = (
            db.query(ServiceCategoryModel)
            .filter(ServiceCategoryModel.name == data.name)
            .first()
        )

        if existing_category:
            raise HTTPException(
                status_code=409,
                detail="Service category already exists"
            )

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return category


@router.delete("/{category_id}", status_code=204)
def delete_service_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admins can delete service categories"
        )

    category = (
        db.query(ServiceCategoryModel)
        .filter(ServiceCategoryModel.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Service category not found"
        )

    db.delete(category)
    db.commit()