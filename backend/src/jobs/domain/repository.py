from abc import ABC, abstractmethod
from uuid import UUID

from src.jobs.domain.entities import Job


class JobFilters:
    def __init__(
        self,
        *,
        search: str | None = None,
        location: str | None = None,
        employment_type: str | None = None,
        experience_level: str | None = None,
        page: int = 1,
        page_size: int = 10,
        sort_by: str = "created_at",
        sort_dir: str = "desc",
    ):
        self.search = search
        self.location = location
        self.employment_type = employment_type
        self.experience_level = experience_level
        self.page = max(page, 1)
        self.page_size = min(max(page_size, 1), 50)
        self.sort_by = sort_by
        self.sort_dir = sort_dir


class JobRepository(ABC):
    @abstractmethod
    def get_by_id(self, job_id: UUID) -> Job | None: ...

    @abstractmethod
    def add(self, job: Job) -> Job: ...

    @abstractmethod
    def list_paginated(self, filters: JobFilters) -> tuple[list[Job], int]: ...

    @abstractmethod
    def delete(self, job: Job) -> None: ...
