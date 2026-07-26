import math
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.auth.domain.entities import User, UserRole
from src.jobs.api.schemas import JobCreateRequest, JobResponse, JobUpdateRequest
from src.jobs.application.service import JobService
from src.jobs.domain.entities import EmploymentType, ExperienceLevel
from src.jobs.domain.repository import JobFilters
from src.shared.database.session import get_db
from src.shared.responses.envelope import Meta, ok
from src.shared.security.dependencies import require_role

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", status_code=201)
def create_job(
    payload: JobCreateRequest,
    current_user: User = Depends(require_role(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    job = JobService(db).create_job(recruiter_id=current_user.id, **payload.model_dump())
    return ok(JobResponse.model_validate(job).model_dump())


@router.get("")
def list_jobs(
    search: str | None = None,
    location: str | None = None,
    employment_type: EmploymentType | None = None,
    experience_level: ExperienceLevel | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    sort_by: str = "created_at",
    sort_dir: str = "desc",
    db: Session = Depends(get_db),
):
    filters = JobFilters(
        search=search,
        location=location,
        employment_type=employment_type.value if employment_type else None,
        experience_level=experience_level.value if experience_level else None,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )
    jobs, total = JobService(db).list_jobs(filters)
    meta = Meta(
        page=filters.page,
        page_size=filters.page_size,
        total=total,
        total_pages=math.ceil(total / filters.page_size) if total else 0,
    )
    return ok([JobResponse.model_validate(j).model_dump() for j in jobs], meta=meta)


@router.get("/{job_id}")
def get_job(job_id: UUID, db: Session = Depends(get_db)):
    job = JobService(db).get_job(job_id)
    return ok(JobResponse.model_validate(job).model_dump())


@router.patch("/{job_id}")
def update_job(
    job_id: UUID,
    payload: JobUpdateRequest,
    current_user: User = Depends(require_role(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    job = JobService(db).update_job(
        job_id=job_id, recruiter_id=current_user.id, **payload.model_dump(exclude_unset=True)
    )
    return ok(JobResponse.model_validate(job).model_dump())


@router.delete("/{job_id}", status_code=204)
def delete_job(
    job_id: UUID,
    current_user: User = Depends(require_role(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    JobService(db).delete_job(job_id=job_id, recruiter_id=current_user.id)
    return None


@router.get("/mine/list")
def list_my_jobs(
    current_user: User = Depends(require_role(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    """Recruiter's own postings, including ones that are closed — not
    exposed via the public /jobs listing which only shows OPEN jobs."""
    from src.jobs.domain.entities import Job  # local import keeps router lean

    jobs = (
        db.query(Job)
        .filter(Job.recruiter_id == current_user.id, Job.is_deleted.is_(False))
        .order_by(Job.created_at.desc())
        .all()
    )
    return ok([JobResponse.model_validate(j).model_dump() for j in jobs])
