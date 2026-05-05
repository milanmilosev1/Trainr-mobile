from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, Query

from app.users.models import User
from app.users.schemas import UpdateUserDTO


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: UUID) -> User | None:
        return self.session.get(User, user_id)

    def get_all(self) -> list[User]:
        return self.session.query(User).all()

    def get_by_email(self, email: str) -> User | None:
        return self.session.query(User).where(User.email == email).first()

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

    def update(self, found: User, dto: UpdateUserDTO) -> User | None:
        try:
            data = dto.model_dump(exclude_unset=True)

            for key, value in data.items():
                if key != "id":
                    setattr(found, key, value)

            found.updated_at = datetime.now(timezone.utc)

            self.session.commit()
            self.session.refresh(found)

            return found

        except SQLAlchemyError:
            self.session.rollback()
            raise
