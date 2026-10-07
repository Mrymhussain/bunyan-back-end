from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.consultation import ConsultationModel
from models.user import UserModel
from serializers.consultation import (
    ConsultationCreateSchema,
    ConsultationSchema,
    ConsultationUpdateSchema,
)

router = APIRouter(prefix="/consultations")


@router.post("", response_model=ConsultationSchema, status_code=201)
def create_consultation(
    data: ConsultationCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != "client":
        raise HTTPException(
            status_code=403,
            detail="Only clients can request consultations"
        )

    engineer = (
        db.query(UserModel)
        .filter(UserModel.id == data.engineer_id)
        .first()
    )

    if not engineer:
        raise HTTPException(
            status_code=404,
            detail="Engineer not found"
        )

    if engineer.role != "engineer":
        raise HTTPException(
            status_code=400,
            detail="Selected user is not an engineer"
        )

    consultation = ConsultationModel(
        client_id=current_user.id,
        engineer_id=data.engineer_id,
        topic=data.topic,
        description=data.description,
        scheduled_at=data.scheduled_at,
        meeting_type=data.meeting_type,
    )

    db.add(consultation)
    db.commit()
    db.refresh(consultation)

    return consultation


@router.get("", response_model=list[ConsultationSchema])
def get_consultations(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role == "admin":
        return db.query(ConsultationModel).all()

    return (
        db.query(ConsultationModel)
        .filter(
            or_(
                ConsultationModel.client_id == current_user.id,
                ConsultationModel.engineer_id == current_user.id,
            )
        )
        .all()
    )


@router.get("/{consultation_id}", response_model=ConsultationSchema)
def get_consultation(
    consultation_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    consultation = (
        db.query(ConsultationModel)
        .filter(ConsultationModel.id == consultation_id)
        .first()
    )

    if not consultation:
        raise HTTPException(
            status_code=404,
            detail="Consultation not found"
        )

    if (
        current_user.role != "admin"
        and consultation.client_id != current_user.id
        and consultation.engineer_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return consultation


@router.put("/{consultation_id}", response_model=ConsultationSchema)
def update_consultation(
    consultation_id: int,
    data: ConsultationUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    consultation = (
        db.query(ConsultationModel)
        .filter(ConsultationModel.id == consultation_id)
        .first()
    )

    if not consultation:
        raise HTTPException(
            status_code=404,
            detail="Consultation not found"
        )

    if (
        consultation.client_id != current_user.id
        and consultation.engineer_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(consultation, key, value)

    db.commit()
    db.refresh(consultation)

    return consultation


@router.delete("/{consultation_id}", status_code=204)
def delete_consultation(
    consultation_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    consultation = (
        db.query(ConsultationModel)
        .filter(ConsultationModel.id == consultation_id)
        .first()
    )

    if not consultation:
        raise HTTPException(
            status_code=404,
            detail="Consultation not found"
        )

    if consultation.client_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    db.delete(consultation)
    db.commit()