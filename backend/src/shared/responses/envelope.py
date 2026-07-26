from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Meta(BaseModel):
    request_id: str | None = None
    page: int | None = None
    page_size: int | None = None
    total: int | None = None
    total_pages: int | None = None


class SuccessEnvelope(BaseModel, Generic[T]):
    success: bool = True
    data: T
    meta: Meta = Meta()


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict[str, Any] | None = None


class ErrorEnvelope(BaseModel):
    success: bool = False
    error: ErrorDetail


def ok(data: Any, meta: Meta | None = None) -> dict:
    return {"success": True, "data": data, "meta": (meta or Meta()).model_dump(exclude_none=True)}


def fail(code: str, message: str, details: dict | None = None) -> dict:
    return {
        "success": False,
        "error": {"code": code, "message": message, "details": details},
    }
