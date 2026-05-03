import uuid

from pydantic import BaseModel, ConfigDict


class CreateExerciseDTO(BaseModel):
    name: str
    description: str
    muscle_group: str
    equipment_type: str

class ExerciseResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str
    muscle_group: str
    equipment_type: str

class UpdateExerciseDTO(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    muscle_group: str
    equipment_type: str