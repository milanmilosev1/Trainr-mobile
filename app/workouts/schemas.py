import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreateWorkoutDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    date: datetime
    name: str
    notes: str
    is_completed: bool

class UpdateWorkoutDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # When updating a workout, we don't need to update user_id because it doesn't make sense
    id: uuid.UUID
    date: datetime
    name: str
    notes: str
    is_completed: bool

class WorkoutResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    date: datetime
    name: str
    notes: str
    is_completed: bool
    created_at: datetime