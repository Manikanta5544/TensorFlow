import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.database.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from src.shared.database.session import Base
from src.shared.database.types import PortableUUID


class ApplicationStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    REVIEWED = "reviewed"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class Application(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "applications"
    __table_args__ = (
        # A candidate can only apply once per job — also our idempotency
        # guard for double-submits (see DECISIONS.md: idempotency).
        UniqueConstraint("job_id", "candidate_id", name="uq_application_job_candidate"),
    )

    job_id: Mapped[uuid.UUID] = mapped_column(
        PortableUUID(), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        PortableUUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    cover_letter: Mapped[str] = mapped_column(Text, nullable=False, default="")
    resume_text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(
            ApplicationStatus, name="application_status", values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False,
        default=ApplicationStatus.SUBMITTED,
    )
