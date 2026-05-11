import uuid

from pydantic import BaseModel, ConfigDict


class CreateShoppingListItemDTO(BaseModel):
    shopping_list_id: uuid.UUID
    ingredient_name: str
    is_checked: bool
    quantity: int

class UpdateShoppingListItemDTO(BaseModel):
    id: uuid.UUID
    shopping_list_id: uuid.UUID
    ingredient_name: str
    is_checked: bool
    quantity: int

class ShoppingListItemResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    shopping_list_id: uuid.UUID
    ingredient_name: str
    is_checked: bool
    quantity: int