import uuid
from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.user_shopping_list.models import UserShoppingList
from app.user_shopping_list.schemas import UpdateUserShoppingListDTO


class UserShoppingListRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, user_shopping_list: UserShoppingList) -> UserShoppingList | None:
        try:
            self.session.add(user_shopping_list)
            self.session.commit()
            self.session.refresh(user_shopping_list)
            return user_shopping_list
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def remove(self, user_shopping_list: UserShoppingList) -> None:
        try:
            self.session.delete(user_shopping_list)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get_by_id(self, user_shopping_list_id: uuid.UUID) -> UserShoppingList | None:
        return self.session.get(UserShoppingList, user_shopping_list_id)

    def get_all(self) -> list[UserShoppingList]:
        return self.session.query(UserShoppingList).all()

    def update(self, found: UserShoppingList, dto: UpdateUserShoppingListDTO) -> UserShoppingList | None:
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