import uuid

from app.shopping_list_items.models import ShoppingListItem
from app.shopping_list_items.repository import ShoppingListItemRepository
from app.shopping_list_items.schemas import CreateShoppingListItemDTO, UpdateShoppingListItemDTO


class ShoppingListItemService:
    def __init__(self, repo: ShoppingListItemRepository):
        self.repo = repo

    def create_new_shopping_list_item(self, dto: CreateShoppingListItemDTO) -> ShoppingListItem:
         item = ShoppingListItem(
             id = uuid.uuid4(),
             shopping_list_id = dto.shopping_list_id,
             ingredient_name = dto.ingredient_name,
             is_checked = dto.is_checked,
             quantity = dto.quantity
         )

         return self.repo.add(item)

    def remove_shopping_list_item(self, shopping_list_item_id: uuid.UUID) -> None:
        item = self.repo.get_by_id(shopping_list_item_id)
        if item is None:
            raise KeyError("Item not found")

        self.repo.remove(item)

    def get_shopping_list_by_id(self, shopping_list_item_id: uuid.UUID) -> ShoppingListItem | None:
        item = self.repo.get_by_id(shopping_list_item_id)
        if item is None:
            raise KeyError("Item not found")

        return item

    def get_all_shopping_list_items(self) -> list[ShoppingListItem]:
        return self.repo.get_all()

    def update_shopping_list_item_info(self, dto: UpdateShoppingListItemDTO):
        found = self.repo.get_by_id(dto.id)

        if found is None:
            raise KeyError("Item does not exist")

        return self.repo.update(found, dto)