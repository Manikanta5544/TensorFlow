from uuid import UUID

from sqlalchemy.orm import Session

from src.auth.domain.entities import User
from src.auth.domain.repository import UserRepository


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: UUID) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email.lower()).first()

    def add(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        return user
