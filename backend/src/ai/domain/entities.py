import enum
import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from src.shared.database.session import Base
from src.shared.database.types import PortableUUID


class AIRequestType(str, enum.Enum):
    JOB_DESCRIPTION = "job_description"


class AIRequest(Base, UUIDPrimaryKeyMixin, TimestampMixin):

    __tablename__ = "ai_requests"

    requester_id: Mapped[uuid.UUID] = mapped_column(
        PortableUUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    request_type: Mapped[AIRequestType] = mapped_column(
        Enum(AIRequestType, name="ai_request_type"), nullable=False
    )
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    succeeded: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
