import uuid


class CreateUserDTO:
    email: str
    name: str
    password_hash: str
    age: int
    weight: int
    height: int

class UpdateUserDTO:
    id: uuid.UUID
    name: str
    password_hash: str
    age: int
    weight: int
    height: int