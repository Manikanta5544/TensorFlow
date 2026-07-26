from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from src.auth.domain.entities import UserRole


class RegisterRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=255)
    role: UserRole
    company_name: str | None = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def validate_recruiter_company(self) -> "RegisterRequest":
        if self.role == UserRole.RECRUITER and not self.company_name:
            raise ValueError("company_name is required when role is 'recruiter'")
        return self


class LoginRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    email: EmailStr
    password: str = Field(min_length=1)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)

    id: UUID
    email: str
    full_name: str
    role: UserRole
    company_name: str | None = None


class AuthResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    user: UserResponse
    access_token: str
    token_type: str = "bearer"
