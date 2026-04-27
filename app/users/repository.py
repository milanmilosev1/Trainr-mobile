from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.users.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: UUID) -> User | None:
        return self.session.get(User, user_id)

    def get_all(self) -> list[User]:
        return self.session.query(User).all()

    def add(self, user: User) -> User:
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def remove(self, user: User) -> None:
        try:
            self.session.delete(user)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def update(self, user: User) -> User | None:
        try:
            found = self.session.get(User, user.id)

            if found is None:
                return None

            found.email = user.email
            found.password_hash = user.password_hash
            found.name = user.name
            found.age = user.age
            found.weight = user.weight
            found.height = user.height
            found.updated_at = datetime.now(timezone.utc)

            self.session.commit()
            self.session.refresh(found)

            return found
        except SQLAlchemyError:
            self.session.rollback()
            raise
