import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.meals.models import MealType


class CreateUserMealPlanDTO(BaseModel):
    user_id: uuid.UUID
    date: datetime
    meal_id: uuid.UUID
    meal_slot: MealType

class UpdateUserMealPlanDTO(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    date: datetime
    meal_id: uuid.UUID
    meal_slot: MealType

class UserMealPlanResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    date: datetime
    meal_id: uuid.UUID
    meal_slot: MealType
    created_at: datetime