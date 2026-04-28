import uuid

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.users.repository import UserRepository
from app.users.schemas import UserResponseDTO, CreateUserDTO, UpdateUserDTO
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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.get("/all", response_model=list[UserResponseDTO], status_code=status.HTTP_200_OK)
def get_all_users(service: UserService = Depends(get_user_service)):
    try:
        return service.get_all_users()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.get("/id", response_model=UserResponseDTO, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: uuid.UUID, service: UserService = Depends(get_user_service)):
    try:
        return service.get_user_by_id(user_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.patch("/update", response_model=UserResponseDTO, status_code=status.HTTP_200_OK)
def update_user_info(user: UpdateUserDTO, service: UserService = Depends(get_user_service)):
    try:
        return service.update_user_info(user)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.delete("/delete", status_code=status.HTTP_200_OK)
def delete_user(user_id: uuid.UUID, service: UserService = Depends(get_user_service)):
    try:
        service.delete_user(user_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))