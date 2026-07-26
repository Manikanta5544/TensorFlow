from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.jobs.domain.entities import EmploymentType, ExperienceLevel, JobStatus


class JobCreateRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str = Field(min_length=3, max_length=255)
    company_name: str = Field(min_length=1, max_length=255)
    location: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=20)
    requirements: str = ""
    employment_type: EmploymentType
    experience_level: ExperienceLevel
    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validate_salary_range(self) -> "JobCreateRequest":
        if self.salary_min is not None and self.salary_max is not None and self.salary_min > self.salary_max:
            raise ValueError("salary_min cannot be greater than salary_max")
        return self


class JobUpdateRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str | None = Field(default=None, min_length=3, max_length=255)
    location: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=20)
    requirements: str | None = None
    employment_type: EmploymentType | None = None
    experience_level: ExperienceLevel | None = None
    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)
    status: JobStatus | None = None


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: UUID
    recruiter_id: UUID
    title: str
    company_name: str
    location: str
    description: str
    requirements: str
    employment_type: EmploymentType
    experience_level: ExperienceLevel
    salary_min: int | None
    salary_max: int | None
    status: JobStatus
    created_at: datetime
    updated_at: datetime


class JobListQuery(BaseModel):
    search: str | None = None
    location: str | None = None
    employment_type: EmploymentType | None = None
    experience_level: ExperienceLevel | None = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=50)
    sort_by: str = "created_at"
    sort_dir: str = "desc"
