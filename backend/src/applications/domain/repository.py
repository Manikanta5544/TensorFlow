from abc import ABC, abstractmethod
from uuid import UUID

from src.applications.domain.entities import Application


class ApplicationRepository(ABC):
    @abstractmethod
    def get_by_id(self, application_id: UUID) -> Application | None: ...

    @abstractmethod
    def get_by_job_and_candidate(self, job_id: UUID, candidate_id: UUID) -> Application | None: ...

    @abstractmethod
    def add(self, application: Application) -> Application: ...

    @abstractmethod
    def list_by_candidate(self, candidate_id: UUID) -> list[Application]: ...

    @abstractmethod
    def list_by_job(self, job_id: UUID) -> list[Application]: ...
