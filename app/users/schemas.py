import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CreateUserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    name: str
    password_hash: str
    age: int
    weight: int
    height: int

class UpdateUserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    password_hash: str
    age: int
    weight: int
    height: int

class UserResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    name: str
    age: int
    weight: int
    height: int
    created_at: datetime
    updated_at: datetime