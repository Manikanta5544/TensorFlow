from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.ai.api.schemas import JobDescriptionGenerateRequest, JobDescriptionGenerateResponse
from src.ai.application.service import AIService
from src.auth.domain.entities import User, UserRole
from src.shared.database.session import get_db
from src.shared.responses.envelope import ok
from src.shared.security.dependencies import require_role

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/job-description")
def generate_job_description(
    payload: JobDescriptionGenerateRequest,
    current_user: User = Depends(require_role(UserRole.RECRUITER)),
    db: Session = Depends(get_db),
):
    text = AIService(db).generate_job_description(
        requester_id=current_user.id,
        role_title=payload.role_title,
        experience_level=payload.experience_level,
        key_skills=payload.key_skills,
    )
    return ok(JobDescriptionGenerateResponse(generated_description=text).model_dump())
