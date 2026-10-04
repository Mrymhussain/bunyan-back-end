from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.project import ProjectModel
from models.user import UserModel
from serializers.project import (
    ProjectCreateSchema,
    ProjectSchema,
    ProjectUpdateSchema,
)

router = APIRouter(prefix="/projects")


@router.post("", response_model=ProjectSchema, status_code=201)
def create_project(
    data: ProjectCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.role != "client":
        raise HTTPException(
            status_code=403,
            detail="Only clients can create projects"
        )

    project = ProjectModel(
        client_id=current_user.id,
        title=data.title,
        project_type=data.project_type,
        description=data.description,
        location=data.location,
        budget_range=data.budget_range,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@router.get("", response_model=list[ProjectSchema])
def get_projects(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return (
        db.query(ProjectModel)
        .filter(ProjectModel.client_id == current_user.id)
        .all()
    )


@router.get("/{project_id}", response_model=ProjectSchema)
def get_project(
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

    return project


@router.put("/{project_id}", response_model=ProjectSchema)
def update_project(
    project_id: int,
    data: ProjectUpdateSchema,
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

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return project