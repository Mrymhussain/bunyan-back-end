from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.project import ProjectModel
from models.project_member import ProjectMemberModel
from models.project_update import ProjectUpdateModel
from models.user import UserModel
from serializers.project_update import (
    ProjectUpdateCreateSchema,
    ProjectUpdateSchema,
)

router = APIRouter(prefix="/projects")


def check_project_access(
    project_id,
    current_user,
    db,
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

    if current_user.role == "admin":
        return project

    if project.client_id == current_user.id:
        return project

    member = (
        db.query(ProjectMemberModel)
        .filter(
            ProjectMemberModel.project_id == project_id,
            ProjectMemberModel.user_id == current_user.id,
        )
        .first()
    )

    if member:
        return project

    raise HTTPException(
        status_code=403,
        detail="Not authorized"
    )


@router.get(
    "/{project_id}/updates",
    response_model=list[ProjectUpdateSchema]
)
def get_project_updates(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    check_project_access(
        project_id,
        current_user,
        db
    )

    updates = (
        db.query(ProjectUpdateModel)
        .filter(
            ProjectUpdateModel.project_id == project_id
        )
        .order_by(ProjectUpdateModel.created_at.desc())
        .all()
    )

    result = []

    for update in updates:
        author = (
            db.query(UserModel)
            .filter(UserModel.id == update.author_id)
            .first()
        )

        result.append({
            "id": update.id,
            "project_id": update.project_id,
            "author_id": update.author_id,
            "author_name": (
                author.name if author else "Unknown User"
            ),
            "author_role": (
                author.role if author else "user"
            ),
            "message": update.message,
            "created_at": update.created_at,
        })

    return result


@router.post(
    "/{project_id}/updates",
    response_model=ProjectUpdateSchema,
    status_code=201
)
def create_project_update(
    project_id: int,
    data: ProjectUpdateCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    check_project_access(
        project_id,
        current_user,
        db
    )

    if not data.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Update cannot be empty"
        )

    update = ProjectUpdateModel(
        project_id=project_id,
        author_id=current_user.id,
        message=data.message.strip(),
    )

    db.add(update)
    db.commit()
    db.refresh(update)

    return {
        "id": update.id,
        "project_id": update.project_id,
        "author_id": update.author_id,
        "author_name": current_user.name,
        "author_role": current_user.role,
        "message": update.message,
        "created_at": update.created_at,
    }
