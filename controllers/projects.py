from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dependencies.get_current_user import get_current_user
from models.project import ProjectModel
from models.project_member import ProjectMemberModel
from models.user import UserModel
from serializers.project import (
    ProjectCreateSchema,
    ProjectMeetingSchema,
    ProjectSchema,
    ProjectUpdateSchema,
    ProjectWorkUpdateSchema,
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


def get_membership(project_id, user_id, db):
    return (
        db.query(ProjectMemberModel)
        .filter(
            ProjectMemberModel.project_id == project_id,
            ProjectMemberModel.user_id == user_id,
        )
        .first()
    )


def can_view_project(project, current_user, db):
    if current_user.role == "admin":
        return True

    if project.client_id == current_user.id:
        return True

    if current_user.role == "engineer":
        return bool(
            get_membership(
                project.id,
                current_user.id,
                db
            )
        )

    return False


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
        image_url=data.image_url,
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
    if current_user.role == "admin":
        return db.query(ProjectModel).all()

    if current_user.role == "engineer":
        return (
            db.query(ProjectModel)
            .join(
                ProjectMemberModel,
                ProjectMemberModel.project_id == ProjectModel.id
            )
            .filter(
                ProjectMemberModel.user_id == current_user.id
            )
            .all()
        )

    if current_user.role == "client":
        return (
            db.query(ProjectModel)
            .filter(
                ProjectModel.client_id == current_user.id
            )
            .all()
        )

    return []


@router.get("/{project_id}", response_model=ProjectSchema)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    project = get_project_or_404(project_id, db)

    if not can_view_project(
        project,
        current_user,
        db
    ):
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
    project = get_project_or_404(project_id, db)

    if (
        current_user.role != "client"
        or project.client_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Only the project owner can edit project details"
        )

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return project


@router.put(
    "/{project_id}/work",
    response_model=ProjectSchema
)
def update_project_work(
    project_id: int,
    data: ProjectWorkUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    project = get_project_or_404(project_id, db)

    if current_user.role == "engineer":
        member = get_membership(
            project_id,
            current_user.id,
            db
        )

        if not member:
            raise HTTPException(
                status_code=403,
                detail="You are not assigned to this project"
            )

    elif current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only assigned engineers or admins can update project work"
        )

    if data.progress is not None:
        if data.progress < 0 or data.progress > 100:
            raise HTTPException(
                status_code=400,
                detail="Progress must be between 0 and 100"
            )

        project.progress = data.progress

    if data.status is not None:
        project.status = data.status

    db.commit()
    db.refresh(project)

    return project


@router.put(
    "/{project_id}/meeting",
    response_model=ProjectSchema
)
def update_project_meeting(
    project_id: int,
    data: ProjectMeetingSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    project = get_project_or_404(project_id, db)

    if current_user.role == "engineer":
        member = get_membership(
            project_id,
            current_user.id,
            db
        )

        if not member:
            raise HTTPException(
                status_code=403,
                detail="You are not assigned to this project"
            )

    elif current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only assigned engineers or admins can schedule meetings"
        )

    if (
        data.meeting_type is not None
        and data.meeting_type not in ["online", "in_person"]
    ):
        raise HTTPException(
            status_code=400,
            detail="Meeting type must be online or in_person"
        )

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    project = get_project_or_404(project_id, db)

    if (
        current_user.role != "client"
        or project.client_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Only the project owner can delete this project"
        )

    db.delete(project)
    db.commit()
