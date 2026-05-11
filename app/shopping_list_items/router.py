import uuid

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.shopping_list_items.repository import ShoppingListItemRepository
from app.shopping_list_items.schemas import ShoppingListItemResponseDTO, CreateShoppingListItemDTO, UpdateShoppingListItemDTO
from app.shopping_list_items.service import ShoppingListItemService

router = APIRouter(prefix = "/shopping_list_items", tags = ["Shopping list items", "Items"])

def get_service(db: Session = Depends(get_db)) -> ShoppingListItemService:
    repo = ShoppingListItemRepository(db)
    return ShoppingListItemService(repo)

@router.get("/all", response_model=list[ShoppingListItemResponseDTO], status_code=status.HTTP_200_OK)
def get_all_items(service: ShoppingListItemService = Depends(get_service)):
    try:
        return service.get_all_shopping_list_items()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.get("/id", response_model=ShoppingListItemResponseDTO, status_code=status.HTTP_200_OK)
def get_item_by_id(item_id: uuid.UUID, service: ShoppingListItemService = Depends(get_service)):
    try:
        return service.get_shopping_list_by_id(item_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.post("/", response_model=ShoppingListItemResponseDTO, status_code=status.HTTP_200_OK)
def add_item(item: CreateShoppingListItemDTO, service: ShoppingListItemService = Depends(get_service)):
    try:
        return service.create_new_shopping_list_item(item)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.patch("/update", response_model=ShoppingListItemResponseDTO, status_code=status.HTTP_200_OK)
def update_item(item: UpdateShoppingListItemDTO, service: ShoppingListItemService = Depends(get_service)):
    try:
        return service.update_shopping_list_item_info(item)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.delete("/delete", status_code=status.HTTP_200_OK)
def remove_item(item: uuid.UUID, service: ShoppingListItemService = Depends(get_service)):
    try:
        service.remove_shopping_list_item(item)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.get("/by-shopping-list", response_model=list[ShoppingListItemResponseDTO], status_code=status.HTTP_200_OK)
def get_all_items_from_shopping_list(shopping_list_id: uuid.UUID, service: ShoppingListItemService = Depends(get_service)):
    try:
        service.get_shopping_list_items_from_user_shopping_list(shopping_list_id)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))