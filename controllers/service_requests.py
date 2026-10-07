from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.service_category import ServiceCategoryModel
from models.service_request import ServiceRequestModel
from models.user import UserModel
from serializers.service_request import (
    ServiceRequestCreateSchema,
    ServiceRequestSchema,
    ServiceRequestUpdateSchema,
)

router = APIRouter(prefix="/service-requests")


def get_request_or_404(request_id, db):
    service_request = (
        db.query(ServiceRequestModel)
        .filter(ServiceRequestModel.id == request_id)
        .first()
    )

    if not service_request:
        raise HTTPException(
            status_code=404,
            detail="Service request not found"
        )

    return service_request


@router.post("", response_model=ServiceRequestSchema, status_code=201)
def create_service_request(
    data: ServiceRequestCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != "client":
        raise HTTPException(
            status_code=403,
            detail="Only clients can create service requests"
        )

    specialist = (
        db.query(UserModel)
        .filter(UserModel.id == data.specialist_id)
        .first()
    )

    if not specialist:
        raise HTTPException(
            status_code=404,
            detail="Specialist not found"
        )

    if specialist.role != "specialist":
        raise HTTPException(
            status_code=400,
            detail="Selected user is not a specialist"
        )

    category = (
        db.query(ServiceCategoryModel)
        .filter(ServiceCategoryModel.id == data.service_category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Service category not found"
        )

    service_request = ServiceRequestModel(
        client_id=current_user.id,
        specialist_id=data.specialist_id,
        service_category_id=data.service_category_id,
        description=data.description,
        location=data.location,
        preferred_date=data.preferred_date,
    )

    db.add(service_request)
    db.commit()
    db.refresh(service_request)

    return service_request


@router.get("", response_model=list[ServiceRequestSchema])
def get_service_requests(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role == "admin":
        return db.query(ServiceRequestModel).all()

    return (
        db.query(ServiceRequestModel)
        .filter(
            or_(
                ServiceRequestModel.client_id == current_user.id,
                ServiceRequestModel.specialist_id == current_user.id,
            )
        )
        .all()
    )


@router.get("/{request_id}", response_model=ServiceRequestSchema)
def get_service_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    service_request = get_request_or_404(request_id, db)

    allowed = (
        current_user.role == "admin"
        or service_request.client_id == current_user.id
        or service_request.specialist_id == current_user.id
    )

    if not allowed:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return service_request


@router.put("/{request_id}", response_model=ServiceRequestSchema)
def update_service_request(
    request_id: int,
    data: ServiceRequestUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    service_request = get_request_or_404(request_id, db)

    update_data = data.model_dump(exclude_unset=True)

    if current_user.role == "client":
        if service_request.client_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized"
            )

        allowed_fields = {
            "description",
            "location",
            "preferred_date",
        }

        update_data = {
            key: value
            for key, value in update_data.items()
            if key in allowed_fields
        }

    elif current_user.role == "specialist":
        if service_request.specialist_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="This request is not assigned to you"
            )

        update_data = {
            key: value
            for key, value in update_data.items()
            if key == "status"
        }

        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="Specialists can only update job status"
            )

        allowed_statuses = [
            "pending",
            "accepted",
            "in_progress",
            "completed",
        ]

        if update_data["status"] not in allowed_statuses:
            raise HTTPException(
                status_code=400,
                detail="Invalid service request status"
            )

    else:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this request"
        )

    for key, value in update_data.items():
        setattr(service_request, key, value)

    db.commit()
    db.refresh(service_request)

    return service_request


@router.delete("/{request_id}", status_code=204)
def delete_service_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    service_request = get_request_or_404(request_id, db)

    if service_request.client_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the client can cancel this request"
        )

    db.delete(service_request)
    db.commit()
