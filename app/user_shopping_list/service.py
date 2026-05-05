import uuid
from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError

from app.user_shopping_list.models import UserShoppingList
from app.user_shopping_list.repository import UserShoppingListRepository
from app.user_shopping_list.schemas import CreateUserShoppingListDTO, UpdateUserShoppingListDTO


class UserShoppingListService:
    def __init__(self, repo: UserShoppingListRepository):
        self.repo = repo

    def get_shopping_list_by_id(self, shopping_list_id: uuid.UUID) -> UserShoppingList:
        try:
            found = self.repo.get_by_id(shopping_list_id)
            if found is None:
                raise KeyError("Shopping list not found")

            return found
        except SQLAlchemyError:
            raise

    def get_all_shopping_lists(self) -> list[UserShoppingList]:
        try:
            return self.repo.get_all()
        except SQLAlchemyError:
            raise

    def create_new_shopping_list(self, shopping_list: CreateUserShoppingListDTO) -> UserShoppingList | None:
        try:
            user_shopping_list = UserShoppingList(
                id = uuid.uuid4(),
                user_id = shopping_list.user_id,
                start_date = shopping_list.start_date,
                end_date = shopping_list.end_date,
                created_at = datetime.now(timezone.utc)
            )
            return self.repo.add(user_shopping_list)
        except SQLAlchemyError:
            raise

    def remove_user_shopping_list(self, user_shopping_list_id: uuid.UUID) -> None:
        try:
            found = self.repo.get_by_id(user_shopping_list_id)
            if found is None:
                raise KeyError("Shopping list not found")

            self.repo.remove(found)
        except SQLAlchemyError:
            raise

    def update_user_shopping_list_info(self, new_shopping_list: UpdateUserShoppingListDTO) -> UserShoppingList | None:
        try:
            found = self.repo.get_by_id(new_shopping_list.id)
            if found is None:
                raise KeyError("Shopping list not found")

            return self.repo.update(found, new_shopping_list)
        except SQLAlchemyError:
            raise