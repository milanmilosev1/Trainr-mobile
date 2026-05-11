import uuid

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.meal_ingredients.repository import MealIngredientRepository
from app.meal_ingredients.schemas import MealIngredientResponseDTO, CreateMealIngredientDTO, UpdateMealIngredientDTO
from app.meal_ingredients.service import MealIngredientService

router = APIRouter(prefix="/meal-ingredients", tags=["Meal ingredient"])

def get_service(db: Session = Depends(get_db)) -> MealIngredientService:
    repo = MealIngredientRepository(db)
    return MealIngredientService(repo)

@router.get("/all", response_model=list[MealIngredientResponseDTO], status_code=status.HTTP_200_OK)
def get_all_igredients(service: MealIngredientService = Depends(get_service)):
    try:
        return service.get_all_meal_ingredients()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.get("/id", response_model=MealIngredientResponseDTO, status_code=status.HTTP_200_OK)
def get_ingredient_by_id(ingredient_id: uuid.UUID, service: MealIngredientService = Depends(get_service)):
    try:
        return service.get_meal_ingredient_by_id(ingredient_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.post("/", response_model=MealIngredientResponseDTO, status_code=status.HTTP_200_OK)
def add_ingredient(ingredient: CreateMealIngredientDTO, service: MealIngredientService = Depends(get_service)):
    try:
        return service.create_new_meal_ingredient(ingredient)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.patch("/update", response_model=MealIngredientResponseDTO, status_code=status.HTTP_200_OK)
def update_ingredient(ingredient: UpdateMealIngredientDTO, service: MealIngredientService = Depends(get_service)):
    try:
        return service.update_meal_ingredient_info(ingredient)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.delete("/delete", status_code=status.HTTP_200_OK)
def remove_ingredient(ingredient: uuid.UUID, service: MealIngredientService = Depends(get_service)):
    try:
        service.remove_meal_ingredient(ingredient)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))
