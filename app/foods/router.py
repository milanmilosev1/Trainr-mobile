import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.foods.repository import FoodRepository
from app.foods.schemas import FoodResponseDTO, CreateFoodDTO, UpdateFoodDTO
from app.foods.service import FoodService

router = APIRouter(prefix="/foods", tags=["Foods"])

def get_food_service(db: Session = Depends(get_db)):
    repo = FoodRepository(db)
    return FoodService(repo)

@router.get("/", response_model=list[FoodResponseDTO], status_code=status.HTTP_200_OK)
def get_all_foods(service: FoodService = Depends(get_food_service)):
    try:
        return service.get_all_foods()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@router.get("/id", response_model=FoodResponseDTO, status_code=status.HTTP_200_OK)
def get_food_by_id(food_id: uuid.UUID, service: FoodService = Depends(get_food_service)):
    try:
        return service.get_food_by_id(food_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Food with id {food_id} not found")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.post("/", response_model=FoodResponseDTO, status_code=status.HTTP_200_OK)
def add_food(food: CreateFoodDTO, service: FoodService = Depends(get_food_service)):
    try:
        return service.create_new_food(food)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.patch("/update", response_model=FoodResponseDTO, status_code=status.HTTP_200_OK)
def update_food(new_food: UpdateFoodDTO, service: FoodService = Depends(get_food_service)):
    try:
        return service.update_food_info(new_food)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Food with id {new_food.id} not found")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.delete("/delete", response_model=None, status_code=status.HTTP_200_OK)
def delete_food(food_id: uuid.UUID, service: FoodService = Depends(get_food_service)):
    try:
        service.remove_food(food_id)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))
