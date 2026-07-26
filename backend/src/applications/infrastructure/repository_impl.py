from uuid import UUID

from sqlalchemy.orm import Session

from src.applications.domain.entities import Application
from src.applications.domain.repository import ApplicationRepository


class SqlAlchemyApplicationRepository(ApplicationRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, application_id: UUID) -> Application | None:
        return self.db.get(Application, application_id)

    def get_by_job_and_candidate(self, job_id: UUID, candidate_id: UUID) -> Application | None:
        return (
            self.db.query(Application)
            .filter(Application.job_id == job_id, Application.candidate_id == candidate_id)
            .first()
        )

    def add(self, application: Application) -> Application:
        self.db.add(application)
        self.db.flush()
        return application

    def list_by_candidate(self, candidate_id: UUID) -> list[Application]:
        return (
            self.db.query(Application)
            .filter(Application.candidate_id == candidate_id)
            .order_by(Application.created_at.desc())
            .all()
        )

    def list_by_job(self, job_id: UUID) -> list[Application]:
        return (
            self.db.query(Application)
            .filter(Application.job_id == job_id)
            .order_by(Application.created_at.desc())
            .all()
        )
