import uuid

from pydantic import BaseModel, ConfigDict


class CreateMealIngredientDTO(BaseModel):
    meal_id: uuid.UUID
    food_id: uuid.UUID
    quantity: int

class UpdateMealIngredientDTO(BaseModel):
    id: uuid.UUID
    meal_id: uuid.UUID
    food_id: uuid.UUID
    quantity: int

class MealIngredientResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    meal_id: uuid.UUID
    food_id: uuid.UUID
    quantity: int