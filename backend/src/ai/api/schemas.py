from pydantic import BaseModel, ConfigDict, Field


class JobDescriptionGenerateRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    role_title: str = Field(min_length=2, max_length=255)
    experience_level: str = Field(min_length=2, max_length=50)
    key_skills: list[str] = Field(min_length=1, max_length=20)


class JobDescriptionGenerateResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    generated_description: str
