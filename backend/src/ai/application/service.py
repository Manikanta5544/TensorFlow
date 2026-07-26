import logging
from uuid import UUID

from sqlalchemy.orm import Session

from src.ai.application.prompts import build_job_description_prompt
from src.ai.domain.entities import AIRequest, AIRequestType
from src.ai.infrastructure.factory import get_llm_provider

logger = logging.getLogger("talentflow.ai")


class AIService:
    """
    AIFacade -> PromptFactory -> LLMProvider -> persisted audit record.
    """

    def __init__(self, db: Session):
        self.db = db
        self.provider = get_llm_provider()

    def generate_job_description(
        self, *, requester_id: UUID, role_title: str, experience_level: str, key_skills: list[str]
    ) -> str:
        request = build_job_description_prompt(
            role_title=role_title, experience_level=experience_level, key_skills=key_skills
        )

        audit = AIRequest(
            requester_id=requester_id,
            request_type=AIRequestType.JOB_DESCRIPTION,
            provider="pending",
            model="pending",
            succeeded=False,
        )

        try:
            result = self.provider.complete(request)
            audit.provider = result.provider
            audit.model = result.model
            audit.succeeded = True
            return result.text
        except Exception:
            audit.succeeded = False
            raise
        finally:
            self.db.add(audit)
            self.db.commit()
            logger.info(
                "ai_request_recorded",
                extra={
                    "extra_fields": {
                        "type": AIRequestType.JOB_DESCRIPTION.value,
                        "succeeded": audit.succeeded,
                    }
                },
            )
