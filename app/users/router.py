from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.users.repository import UserRepository
from app.users.schemas import UserResponseDTO, CreateUserDTO
from app.users.service import UserService

router = APIRouter(prefix="/users",tags=["Users"])

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)

@router.post("/", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
def add_user(new_user: CreateUserDTO, service: UserService = Depends(get_user_service)):
    try:
        return service.create_new_user(new_user)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )
