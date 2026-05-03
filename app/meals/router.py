import uuid

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.db_connection import get_db

from app.meals.repository import MealRepository
from app.meals.schemas import MealResponseDTO, CreateMealDTO, UpdateMealDTO
from app.meals.service import MealService

router = APIRouter(prefix="/meals",tags=["Meals"])

def get_meal_service(db: Session = Depends(get_db)) -> MealService:
    repo = MealRepository(db)
    return MealService(repo)

@router.get("/all", response_model=list[MealResponseDTO], status_code=status.HTTP_200_OK)
def get_all_meals(service: MealService = Depends(get_meal_service)):
    try:
        return service.get_all_meals()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.get("/id", response_model=MealResponseDTO, status_code=status.HTTP_200_OK)
def get_meal_by_id(meal_id: uuid.UUID, service: MealService = Depends(get_meal_service)):
    try:
        return service.get_meal_by_id(meal_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.post("/", response_model=MealResponseDTO, status_code=status.HTTP_200_OK)
def add_meal(meal: CreateMealDTO, service: MealService = Depends(get_meal_service)):
    try:
        return service.create_new_meal(meal)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.delete("/delete", status_code=status.HTTP_200_OK)
def remove_meal(meal_id: uuid.UUID, service: MealService = Depends(get_meal_service)):
    try:
        service.delete_meal(meal_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.patch("/update", response_model=MealResponseDTO, status_code=status.HTTP_200_OK)
def update_meal(meal: UpdateMealDTO, service: MealService = Depends(get_meal_service)):
    try:
        return service.update_meal(meal)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))