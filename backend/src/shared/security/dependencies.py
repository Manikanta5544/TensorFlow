from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from src.auth.domain.entities import User, UserRole
from src.auth.infrastructure.repository_impl import SqlAlchemyUserRepository
from src.shared.database.session import get_db
from src.shared.exceptions.exceptions import ForbiddenError, UnauthorizedError
from src.shared.security.security import decode_access_token

_bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise UnauthorizedError("Authentication required.", code="MISSING_TOKEN")

    try:
        token_payload = decode_access_token(credentials.credentials)
    except JWTError as exc:
        raise UnauthorizedError("Invalid or expired token.", code="INVALID_TOKEN") from exc

    user = SqlAlchemyUserRepository(db).get_by_id(UUID(token_payload.sub))
    if user is None or not user.is_active:
        raise UnauthorizedError("Invalid or expired token.", code="INVALID_TOKEN")

    return user


def require_role(*allowed_roles: UserRole):

    def _guard(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise ForbiddenError(
                f"This action requires one of these roles: {[r.value for r in allowed_roles]}.",
                code="INSUFFICIENT_ROLE",
            )
        return current_user

    return _guard
