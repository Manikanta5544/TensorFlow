import logging

from sqlalchemy.orm import Session

from src.auth.domain.entities import User, UserRole
from src.auth.infrastructure.repository_impl import SqlAlchemyUserRepository
from src.shared.exceptions.exceptions import ConflictError, UnauthorizedError
from src.shared.security.security import (
    create_access_token,
    hash_password,
    verify_password,
)

logger = logging.getLogger("tensorflow.auth")


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = SqlAlchemyUserRepository(db)

    def register(
        self,
        *,
        email: str,
        password: str,
        full_name: str,
        role: UserRole,
        company_name: str | None,
    ) -> tuple[User, str]:
        normalized_email = email.lower().strip()

        if self.repo.get_by_email(normalized_email):
            raise ConflictError("An account with this email already exists.", code="EMAIL_TAKEN")

        if role == UserRole.RECRUITER and not company_name:
            raise ConflictError("company_name is required for recruiter accounts.", code="COMPANY_REQUIRED")

        user = User(
            email=normalized_email,
            hashed_password=hash_password(password),
            full_name=full_name.strip(),
            role=role,
            company_name=company_name.strip() if company_name else None,
        )
        self.repo.add(user)
        self.db.commit()
        self.db.refresh(user)

        logger.info("user_registered", extra={"extra_fields": {"user_id": str(user.id), "role": role.value}})

        token = create_access_token(subject=user.id, role=user.role.value)
        return user, token

    def login(self, *, email: str, password: str) -> tuple[User, str]:
        user = self.repo.get_by_email(email.lower().strip())

        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password.", code="INVALID_CREDENTIALS")

        if not user.is_active:
            raise UnauthorizedError("This account has been deactivated.", code="ACCOUNT_INACTIVE")

        logger.info("user_logged_in", extra={"extra_fields": {"user_id": str(user.id)}})

        token = create_access_token(subject=user.id, role=user.role.value)
        return user, token
