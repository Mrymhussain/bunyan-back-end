from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.project import ProjectModel
from models.project_member import ProjectMemberModel
from models.user import UserModel
from serializers.project_member import (
    ProjectMemberApprovalSchema,
    ProjectMemberCreateSchema,
    ProjectMemberSchema,
)

router = APIRouter(prefix="/projects")


def get_project_or_404(project_id, db):
    project = (
        db.query(ProjectModel)
        .filter(ProjectModel.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


def is_project_member(project_id, user_id, db):
    return (
        db.query(ProjectMemberModel)
        .filter(
            ProjectMemberModel.project_id == project_id,
            ProjectMemberModel.user_id == user_id,
        )
        .first()
    )


@router.get(
    "/{project_id}/members",
    response_model=list[ProjectMemberSchema]
)
def get_project_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    project = get_project_or_404(project_id, db)

    allowed = (
        current_user.role == "admin"
        or project.client_id == current_user.id
        or is_project_member(
            project_id,
            current_user.id,
            db
        )
    )

    if not allowed:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    members = (
        db.query(ProjectMemberModel)
        .filter(
            ProjectMemberModel.project_id == project_id
        )
        .all()
    )

    result = []

    for member in members:
        user = (
            db.query(UserModel)
            .filter(UserModel.id == member.user_id)
            .first()
        )

        result.append({
            "id": member.id,
            "project_id": member.project_id,
            "user_id": member.user_id,
            "discipline": member.discipline,
            "approved": member.approved,
            "approval_note": member.approval_note,
            "user_name": user.name if user else None,
            "user_specialty": user.specialty if user else None,
            "user_image_url": user.image_url if user else None,
        })

    return result


@router.post(
    "/{project_id}/members",
    response_model=ProjectMemberSchema,
    status_code=201
)
def add_project_member(
    project_id: int,
    data: ProjectMemberCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    get_project_or_404(project_id, db)

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admins can assign engineers"
        )

    user = (
        db.query(UserModel)
        .filter(UserModel.id == data.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role != "engineer":
        raise HTTPException(
            status_code=400,
            detail="Project member must be an engineer"
        )

    existing_member = (
        db.query(ProjectMemberModel)
        .filter(
            ProjectMemberModel.project_id == project_id,
            ProjectMemberModel.user_id == data.user_id,
        )
        .first()
    )

    if existing_member:
        raise HTTPException(
            status_code=409,
            detail="Engineer is already assigned"
        )

    member = ProjectMemberModel(
        project_id=project_id,
        user_id=data.user_id,
        discipline=data.discipline,
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return {
        "id": member.id,
        "project_id": member.project_id,
        "user_id": member.user_id,
        "discipline": member.discipline,
        "approved": member.approved,
        "approval_note": member.approval_note,
        "user_name": user.name,
        "user_specialty": user.specialty,
        "user_image_url": user.image_url,
    }


@router.put(
    "/{project_id}/members/{member_id}/approval",
    response_model=ProjectMemberSchema
)
def update_member_approval(
    project_id: int,
    member_id: int,
    data: ProjectMemberApprovalSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    get_project_or_404(project_id, db)

    member = (
        db.query(ProjectMemberModel)
        .filter(
            ProjectMemberModel.id == member_id,
            ProjectMemberModel.project_id == project_id,
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Project member not found"
        )

    if member.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only approve your own discipline"
        )

    member.approved = data.approved
    member.approval_note = data.approval_note

    db.commit()
    db.refresh(member)

    user = (
        db.query(UserModel)
        .filter(UserModel.id == member.user_id)
        .first()
    )

    return {
        "id": member.id,
        "project_id": member.project_id,
        "user_id": member.user_id,
        "discipline": member.discipline,
        "approved": member.approved,
        "approval_note": member.approval_note,
        "user_name": user.name if user else None,
        "user_specialty": user.specialty if user else None,
        "user_image_url": user.image_url if user else None,
    }


@router.delete(
    "/{project_id}/members/{member_id}",
    status_code=204
)
def remove_project_member(
    project_id: int,
    member_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    get_project_or_404(project_id, db)

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admins can remove engineers"
        )

    member = (
        db.query(ProjectMemberModel)
        .filter(
            ProjectMemberModel.id == member_id,
            ProjectMemberModel.project_id == project_id,
        )
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Project member not found"
        )

    db.delete(member)
    db.commit()
