import uuid

from pydantic import BaseModel, ConfigDict


class UpdateFoodDTO(BaseModel):
    id: uuid.UUID
    name: str
    calories_per_serving: int
    protein_g: int
    carbs_g: int
    fat_g: int
    serving_size: str

class CreateFoodDTO(BaseModel):
    name: str
    calories_per_serving: int
    protein_g: int
    carbs_g: int
    fat_g: int
    serving_size: str

class FoodResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    calories_per_serving: int
    protein_g: int
    carbs_g: int
    fat_g: int
    serving_size: str
