from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.applications.api.schemas import (
    ApplicationResponse,
    ApplicationStatusUpdateRequest,
    ApplyRequest,
)
from src.applications.application.service import ApplicationService
from src.auth.domain.entities import User, UserRole
from src.shared.database.session import get_db
from src.shared.responses.envelope import ok
from src.shared.security.dependencies import require_role

router = APIRouter(tags=["applications"])


@router.post("/jobs/{job_id}/applications", status_code=201)
def apply_to_job(
    job_id: UUID,
    payload: ApplyRequest,
    current_user: User = Depends(require_role(UserRole.CANDIDATE)),
    db: Session = Depends(get_db),
):
    application = ApplicationService(db).apply(
        job_id=job_id,
        candidate_id=current_user.id,
        cover_letter=payload.cover_letter,
        resume_text=payload.resume_text,
    )
    return ok(ApplicationResponse.model_validate(application).model_dump())


@router.get("/jobs/{job_id}/applications")
def list_applications_for_job(
    job_id: UUID,
    current_user: User = Depends(require_role(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    applications = ApplicationService(db).list_applications_for_job(
        job_id=job_id, recruiter_id=current_user.id
    )
    return ok([ApplicationResponse.model_validate(a).model_dump() for a in applications])


@router.get("/applications/mine")
def list_my_applications(
    current_user: User = Depends(require_role(UserRole.CANDIDATE)),
    db: Session = Depends(get_db),
):
    applications = ApplicationService(db).list_my_applications(current_user.id)
    return ok([ApplicationResponse.model_validate(a).model_dump() for a in applications])


@router.patch("/applications/{application_id}/status")
def update_application_status(
    application_id: UUID,
    payload: ApplicationStatusUpdateRequest,
    current_user: User = Depends(require_role(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    application = ApplicationService(db).update_status(
        application_id=application_id, recruiter_id=current_user.id, status=payload.status
    )
    return ok(ApplicationResponse.model_validate(application).model_dump())
