import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UpdateUserShoppingListDTO(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    start_date: datetime
    end_date: datetime
    created_at: datetime

class CreateUserShoppingListDTO(BaseModel):
    user_id: uuid.UUID
    start_date: datetime
    end_date: datetime

class UserShoppingListResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    start_date: datetime
    end_date: datetime
    created_at: datetime