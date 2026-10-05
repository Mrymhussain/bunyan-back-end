from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.material import MaterialModel
from models.user import UserModel
from serializers.material import (
    MaterialCreateSchema,
    MaterialSchema,
    MaterialUpdateSchema,
)

router = APIRouter(prefix="/materials")


@router.get("", response_model=list[MaterialSchema])
def get_materials(
    db: Session = Depends(get_db),
):
    return db.query(MaterialModel).all()


@router.get("/{material_id}", response_model=MaterialSchema)
def get_material(
    material_id: int,
    db: Session = Depends(get_db),
):
    material = (
        db.query(MaterialModel)
        .filter(MaterialModel.id == material_id)
        .first()
    )

    if not material:
        raise HTTPException(
            status_code=404,
            detail="Material not found"
        )

    return material


@router.post("", response_model=MaterialSchema, status_code=201)
def create_material(
    data: MaterialCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != "supplier":
        raise HTTPException(
            status_code=403,
            detail="Only suppliers can create materials"
        )

    material = MaterialModel(
        supplier_id=current_user.id,
        name=data.name,
        category=data.category,
        description=data.description,
        price=data.price,
        stock_quantity=data.stock_quantity,
    )

    db.add(material)
    db.commit()
    db.refresh(material)

    return material


@router.put("/{material_id}", response_model=MaterialSchema)
def update_material(
    material_id: int,
    data: MaterialUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    material = (
        db.query(MaterialModel)
        .filter(MaterialModel.id == material_id)
        .first()
    )

    if not material:
        raise HTTPException(
            status_code=404,
            detail="Material not found"
        )

    if material.supplier_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(material, key, value)

    db.commit()
    db.refresh(material)

    return material


@router.delete("/{material_id}", status_code=204)
def delete_material(
    material_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    material = (
        db.query(MaterialModel)
        .filter(MaterialModel.id == material_id)
        .first()
    )

    if not material:
        raise HTTPException(
            status_code=404,
            detail="Material not found"
        )

    if material.supplier_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    db.delete(material)
    db.commit()