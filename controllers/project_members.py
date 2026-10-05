from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.project import ProjectModel
from models.project_member import ProjectMemberModel
from models.user import UserModel
from serializers.project_member import (
    ProjectMemberCreateSchema,
    ProjectMemberSchema,
)

router = APIRouter(prefix="/projects")


@router.get(
    "/{project_id}/members",
    response_model=list[ProjectMemberSchema]
)
def get_project_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
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

    if project.client_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return (
        db.query(ProjectMemberModel)
        .filter(ProjectMemberModel.project_id == project_id)
        .all()
    )


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

    if project.client_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
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
            detail="User is already a project member"
        )

    member = ProjectMemberModel(
        project_id=project_id,
        user_id=data.user_id,
        discipline=data.discipline,
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member


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

    if project.client_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
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
    