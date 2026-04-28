import uuid

from pydantic import ConfigDict, BaseModel

from app.meals.models import MealType, MealDifficulty


class CreateMealDTO(BaseModel):
    name: str
    meal_type: MealType
    calories: int
    protein_g: int
    carbs_g: int
    fat_g: int
    cook_time_minutes: int
    difficulty: MealDifficulty
    tags: list[str]

class UpdateMealDTO(BaseModel):
    id: uuid.UUID
    name: str
    meal_type: MealType
    calories: int
    protein_g: int
    carbs_g: int
    fat_g: int
    cook_time_minutes: int
    difficulty: MealDifficulty
    tags: list[str]

class MealResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    meal_type: MealType
    calories: int
    protein_g: int
    carbs_g: int
    fat_g: int
    cook_time_minutes: int
    difficulty: MealDifficulty
    tags: list[str]
