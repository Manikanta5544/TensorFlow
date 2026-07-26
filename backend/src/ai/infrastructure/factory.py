from src.ai.domain.provider import LLMProvider
from src.ai.infrastructure.providers import MockLLMProvider, OpenAICompatibleProvider
from src.shared.config.settings import get_settings


def get_llm_provider() -> LLMProvider:
    settings = get_settings()

    if settings.AI_PROVIDER == "openai_compatible" and settings.AI_API_KEY:
        return OpenAICompatibleProvider(
            api_key=settings.AI_API_KEY,
            base_url=settings.AI_BASE_URL,
            model=settings.AI_MODEL,
        )

    return MockLLMProvider()
