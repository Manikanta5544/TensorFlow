from uuid import UUID

from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from src.jobs.domain.entities import Job, JobStatus
from src.jobs.domain.repository import JobFilters, JobRepository

_SORTABLE_COLUMNS = {
    "created_at": Job.created_at,
    "title": Job.title,
    "salary_min": Job.salary_min,
}


class SqlAlchemyJobRepository(JobRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, job_id: UUID) -> Job | None:
        job = self.db.get(Job, job_id)
        if job is None or job.is_deleted:
            return None
        return job

    def add(self, job: Job) -> Job:
        self.db.add(job)
        self.db.flush()
        return job

    def delete(self, job: Job) -> None:
        # Soft delete — see brief: "soft deletes where appropriate".
        job.is_deleted = True
        self.db.flush()

    def list_paginated(self, filters: JobFilters) -> tuple[list[Job], int]:
        query = self.db.query(Job).filter(Job.is_deleted.is_(False), Job.status == JobStatus.OPEN)

        if filters.search:
            like = f"%{filters.search}%"
            query = query.filter(or_(Job.title.ilike(like), Job.description.ilike(like)))
        if filters.location:
            query = query.filter(Job.location.ilike(f"%{filters.location}%"))
        if filters.employment_type:
            query = query.filter(Job.employment_type == filters.employment_type)
        if filters.experience_level:
            query = query.filter(Job.experience_level == filters.experience_level)

        total = query.count()

        sort_column = _SORTABLE_COLUMNS.get(filters.sort_by, Job.created_at)
        order_fn = asc if filters.sort_dir == "asc" else desc
        query = query.order_by(order_fn(sort_column))

        offset = (filters.page - 1) * filters.page_size
        items = query.offset(offset).limit(filters.page_size).all()

        return items, total
