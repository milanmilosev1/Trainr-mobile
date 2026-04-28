import uuid
from datetime import datetime, timezone

from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import CreateUserDTO
from app.users.schemas import UpdateUserDTO


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_new_user(self, new_user: CreateUserDTO) -> User:
        existing = self.repo.get_by_email(new_user.email)
        if existing is not None:
            raise ValueError("User already exists")

        user = User(
            id=uuid.uuid4(),
            email=new_user.email,
            password_hash=new_user.password_hash,
            name=new_user.name,
            age=new_user.age,
            weight=new_user.weight,
            height=new_user.height,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        return self.repo.add(user)

    def delete_user(self, user_id: uuid.UUID) -> None:
        user = self.repo.get_by_id(user_id)
        if user is None:
            raise KeyError("User not found")

        self.repo.remove(user)

    def update_user_info(self, new_user: UpdateUserDTO) -> User:
        user = self.repo.get_by_id(new_user.id)

        if user is None:
            raise KeyError("User not found")

        user.name = new_user.name
        user.age = new_user.age
        user.height = new_user.height
        user.weight = new_user.weight
        user.password_hash = new_user.password_hash
        user.updated_at = datetime.now(timezone.utc)

        success = self.repo.update(user)

        if not success:
            raise ValueError("Failed to update user")

        return success

    def get_all_users(self) -> list[User]:
        return self.repo.get_all()

    def get_user_by_id(self, user_id: uuid.UUID) -> User:
        user = self.repo.get_by_id(user_id)

        if user is None:
            raise KeyError("User not found")

        return user