import uuid

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.user_meal_plans.repository import UserMealPlanRepository
from app.user_meal_plans.schemas import UserMealPlanResponseDTO, CreateUserMealPlanDTO, UpdateUserMealPlanDTO
from app.user_meal_plans.service import UserMealPlanService

router = APIRouter(prefix="/user-meal-plans", tags=["User meal plans"])

def get_service(db: Session = Depends(get_db)) -> UserMealPlanService:
    repo = UserMealPlanRepository(db)
    return UserMealPlanService(repo)

@router.get("/all", response_model=list[UserMealPlanResponseDTO], status_code=status.HTTP_200_OK)
def get_all_meal_plans(service: UserMealPlanService = Depends(get_service)):
    try:
        return service.get_all_user_meal_plans()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.get("/id", response_model=UserMealPlanResponseDTO, status_code=status.HTTP_200_OK)
def get_meal_plan_by_id(meal_plan_id: uuid.UUID, service: UserMealPlanService = Depends(get_service)):
    try:
        return service.get_user_meal_plan_by_id(meal_plan_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.get("/user-id", response_model=list[UserMealPlanResponseDTO], status_code=status.HTTP_200_OK)
def get_meal_plan_by_user_id(user_id: uuid.UUID, service: UserMealPlanService = Depends(get_service)):
    try:
        return service.get_user_meal_plan_by_user_id(user_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))


@router.post("/", response_model=UserMealPlanResponseDTO, status_code=status.HTTP_200_OK)
def add_meal_plan(meal_plan: CreateUserMealPlanDTO, service: UserMealPlanService = Depends(get_service)):
    try:
        return service.create_new_user_meal_plan(meal_plan)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.patch("/update", response_model=UserMealPlanResponseDTO, status_code=status.HTTP_200_OK)
def update_meal_plan(meal_plan: UpdateUserMealPlanDTO, service: UserMealPlanService = Depends(get_service)):
    try:
        return service.update_user_meal_plan_info(meal_plan)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.delete("/delete", status_code=status.HTTP_200_OK)
def remove_meal_plan(meal_id: uuid.UUID, service: UserMealPlanService = Depends(get_service)):
    try:
        service.remove_user_meal_plan(meal_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))