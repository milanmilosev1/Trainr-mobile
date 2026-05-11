import uuid

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.shopping_list_items.models import ShoppingListItem
from app.shopping_list_items.schemas import UpdateShoppingListItemDTO


class ShoppingListItemRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, shopping_list_item: ShoppingListItem) -> ShoppingListItem:
        try:
            self.session.add(shopping_list_item)
            self.session.commit()
            self.session.refresh(shopping_list_item)
            return shopping_list_item
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get_by_id(self, item_id: uuid.UUID) -> ShoppingListItem | None:
        return self.session.get(ShoppingListItem, item_id);

    def get_all(self) -> list[ShoppingListItem]:
        return self.session.query(ShoppingListItem).all()

    def remove(self, shopping_list_item: ShoppingListItem) -> None:
        try:
            self.session.delete(shopping_list_item)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def update(self, found: ShoppingListItem, dto: UpdateShoppingListItemDTO) -> ShoppingListItem:
        try:
            data = dto.model_dump(exclude_unset=True)

            for key, value in data.items():
                if key != "id":
                    setattr(found, key, value)

            self.session.commit()
            self.session.refresh(found)

            return found

        except SQLAlchemyError:
            self.session.rollback()
            raise

