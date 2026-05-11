import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreateUserFavouriteMealDTO(BaseModel):
    user_id: uuid.UUID
    meal_id: uuid.UUID

class UpdateUserFavouriteMealDTO(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    meal_id: uuid.UUID

class UserFavouriteMealResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    meal_id: uuid.UUID
    created_at: datetime