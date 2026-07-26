from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.applications.domain.entities import ApplicationStatus


class ApplyRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    cover_letter: str = Field(default="", max_length=5000)
    resume_text: str = Field(min_length=20, max_length=20000)


class ApplicationStatusUpdateRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    status: ApplicationStatus


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: UUID
    job_id: UUID
    candidate_id: UUID
    cover_letter: str
    resume_text: str
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime
