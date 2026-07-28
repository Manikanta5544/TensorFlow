import logging
from uuid import UUID

from sqlalchemy.orm import Session

from src.jobs.domain.entities import Job
from src.jobs.domain.repository import JobFilters
from src.jobs.infrastructure.repository_impl import SqlAlchemyJobRepository
from src.shared.exceptions.exceptions import ForbiddenError, NotFoundError

logger = logging.getLogger("tensorflow.jobs")


class JobService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = SqlAlchemyJobRepository(db)

    def create_job(self, *, recruiter_id: UUID, **fields) -> Job:
        job = Job(recruiter_id=recruiter_id, **fields)
        self.repo.add(job)
        self.db.commit()
        self.db.refresh(job)
        logger.info(
            "job_created", extra={"extra_fields": {"job_id": str(job.id), "recruiter_id": str(recruiter_id)}}
        )
        return job

    def get_job(self, job_id: UUID) -> Job:
        job = self.repo.get_by_id(job_id)
        if job is None:
            raise NotFoundError("Job not found.", code="JOB_NOT_FOUND")
        return job

    def list_jobs(self, filters: JobFilters) -> tuple[list[Job], int]:
        return self.repo.list_paginated(filters)

    def update_job(self, *, job_id: UUID, recruiter_id: UUID, **fields) -> Job:
        job = self.get_job(job_id)
        self._assert_owner(job, recruiter_id)
        for key, value in fields.items():
            if value is not None:
                setattr(job, key, value)
        self.db.commit()
        self.db.refresh(job)
        logger.info("job_updated", extra={"extra_fields": {"job_id": str(job.id)}})
        return job

    def delete_job(self, *, job_id: UUID, recruiter_id: UUID) -> None:
        job = self.get_job(job_id)
        self._assert_owner(job, recruiter_id)
        self.repo.delete(job)
        self.db.commit()
        logger.info("job_deleted", extra={"extra_fields": {"job_id": str(job.id)}})

    @staticmethod
    def _assert_owner(job: Job, recruiter_id: UUID) -> None:
        if job.recruiter_id != recruiter_id:
            raise ForbiddenError("You do not own this job posting.", code="NOT_JOB_OWNER")
