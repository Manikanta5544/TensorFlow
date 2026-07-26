"""
Provider abstraction (ADR-006).

The application layer only ever talks to `LLMProvider`. Swapping OpenAI
for Groq, Anthropic, or a local model means writing one new adapter in
infrastructure/ — zero changes to services, routers, or prompts.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class CompletionRequest:
    system_prompt: str
    user_prompt: str
    max_tokens: int = 800
    temperature: float = 0.4


@dataclass(frozen=True)
class CompletionResult:
    text: str
    provider: str
    model: str


class LLMProvider(ABC):
    @abstractmethod
    def complete(self, request: CompletionRequest) -> CompletionResult: ...
