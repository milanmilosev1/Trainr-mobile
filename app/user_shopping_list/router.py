import uuid

from fastapi import APIRouter, status, Depends, HTTPException

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.user_shopping_list.repository import UserShoppingListRepository
from app.user_shopping_list.schemas import UserShoppingListResponseDTO, CreateUserShoppingListDTO, \
    UpdateUserShoppingListDTO
from app.user_shopping_list.service import UserShoppingListService


router = APIRouter(prefix="/user_shopping_list", tags=["User Shopping Lists"])

def get_user_shopping_list_service(db: Session = Depends(get_db)):
    repo = UserShoppingListRepository(db)
    return UserShoppingListService(repo)

@router.get("/all", response_model = list[UserShoppingListResponseDTO], status_code = status.HTTP_200_OK)
def get_all_shopping_lists(service: UserShoppingListService = Depends(get_user_shopping_list_service)):
    try:
        return service.get_all_shopping_lists()
    except SQLAlchemyError as error:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(error))

@router.get("/id", response_model = UserShoppingListResponseDTO, status_code = status.HTTP_200_OK)
def get_shopping_list_by_id(shopping_list_id: uuid.UUID, service: UserShoppingListService = Depends(get_user_shopping_list_service)):
    try:
        return service.get_shopping_list_by_id(shopping_list_id)
    except KeyError as error:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Shopping list with the id {shopping_list_id} is not found")
    except SQLAlchemyError as error:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(error))

@router.post("/", response_model = UserShoppingListResponseDTO, status_code = status.HTTP_200_OK)
def add_shopping_list(shopping_list: CreateUserShoppingListDTO, service: UserShoppingListService = Depends(get_user_shopping_list_service)):
    try:
        return service.create_new_shopping_list(shopping_list)
    except SQLAlchemyError as error:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(error))

@router.patch("/update", response_model = UserShoppingListResponseDTO, status_code = status.HTTP_200_OK)
def update_shopping_list_info(new_shopping_list: UpdateUserShoppingListDTO, service: UserShoppingListService = Depends(get_user_shopping_list_service)):
    try:
        return service.update_user_shopping_list_info(new_shopping_list)
    except KeyError as error:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Shopping list with id: {new_shopping_list.id} not found")
    except SQLAlchemyError as error:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(error))

@router.delete("/delete", response_model = None, status_code = status.HTTP_200_OK)
def delete_shopping_list(shopping_list_id: uuid.UUID, service: UserShoppingListService = Depends(get_user_shopping_list_service)):
    try:
        service.remove_user_shopping_list(shopping_list_id)
    except SQLAlchemyError as error:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(error))