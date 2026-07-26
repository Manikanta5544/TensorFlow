import logging
from uuid import UUID

from sqlalchemy.orm import Session

from src.applications.domain.entities import Application, ApplicationStatus
from src.applications.infrastructure.repository_impl import SqlAlchemyApplicationRepository
from src.jobs.application.service import JobService
from src.shared.exceptions.exceptions import ConflictError, ForbiddenError, NotFoundError

logger = logging.getLogger("talentflow.applications")


class ApplicationService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = SqlAlchemyApplicationRepository(db)
        self.job_service = JobService(db)

    def apply(self, *, job_id: UUID, candidate_id: UUID, cover_letter: str, resume_text: str) -> Application:
        # Ensures the job exists and is not soft-deleted (raises NotFoundError otherwise).
        self.job_service.get_job(job_id)

        # Idempotency: applying twice to the same job is a conflict, not a
        # silent duplicate row — see DECISIONS.md on idempotency.
        if self.repo.get_by_job_and_candidate(job_id, candidate_id):
            raise ConflictError("You have already applied to this job.", code="ALREADY_APPLIED")

        application = Application(
            job_id=job_id,
            candidate_id=candidate_id,
            cover_letter=cover_letter,
            resume_text=resume_text,
        )
        self.repo.add(application)
        self.db.commit()
        self.db.refresh(application)
        logger.info(
            "application_submitted",
            extra={"extra_fields": {"application_id": str(application.id), "job_id": str(job_id)}},
        )
        return application

    def list_my_applications(self, candidate_id: UUID) -> list[Application]:
        return self.repo.list_by_candidate(candidate_id)

    def list_applications_for_job(self, *, job_id: UUID, recruiter_id: UUID) -> list[Application]:
        job = self.job_service.get_job(job_id)
        if job.recruiter_id != recruiter_id:
            raise ForbiddenError("You do not own this job posting.", code="NOT_JOB_OWNER")
        return self.repo.list_by_job(job_id)

    def update_status(
        self, *, application_id: UUID, recruiter_id: UUID, status: ApplicationStatus
    ) -> Application:
        application = self.repo.get_by_id(application_id)
        if application is None:
            raise NotFoundError("Application not found.", code="APPLICATION_NOT_FOUND")

        job = self.job_service.get_job(application.job_id)
        if job.recruiter_id != recruiter_id:
            raise ForbiddenError("You do not own this job posting.", code="NOT_JOB_OWNER")

        application.status = status
        self.db.commit()
        self.db.refresh(application)
        logger.info(
            "application_status_updated",
            extra={"extra_fields": {"application_id": str(application_id), "status": status.value}},
        )
        return application
