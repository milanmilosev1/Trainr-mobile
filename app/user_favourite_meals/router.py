import uuid

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.user_favourite_meals.repository import UserFavouriteMealRepository
from app.user_favourite_meals.schemas import UserFavouriteMealResponseDTO, CreateUserFavouriteMealDTO, \
    UpdateUserFavouriteMealDTO
from app.user_favourite_meals.service import UserFavouriteMealService

router = APIRouter(prefix="/user-favourite-meals", tags=["User favourite meals"])

def get_service(db: Session = Depends(get_db)) -> UserFavouriteMealService:
    repo = UserFavouriteMealRepository(db)
    return UserFavouriteMealService(repo)

@router.get("/all", response_model=list[UserFavouriteMealResponseDTO], status_code=status.HTTP_200_OK)
def get_all_meals(service: UserFavouriteMealService = Depends(get_service)):
    try:
        return service.get_all_user_favourite_meals()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.get("/id", response_model=UserFavouriteMealResponseDTO, status_code=status.HTTP_200_OK)
def get_meals_by_id(item_id: uuid.UUID, service: UserFavouriteMealService = Depends(get_service)):
    try:
        return service.get_user_favourite_meal_by_id(item_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.post("/", response_model=UserFavouriteMealResponseDTO, status_code=status.HTTP_200_OK)
def add_user_favourite_meal(item: CreateUserFavouriteMealDTO, service: UserFavouriteMealService = Depends(get_service)):
    try:
        return service.create_user_favourite_meal(item)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.patch("/update", response_model=UserFavouriteMealResponseDTO, status_code=status.HTTP_200_OK)
def update_meal(item: UpdateUserFavouriteMealDTO, service: UserFavouriteMealService = Depends(get_service)):
    try:
        return service.update_user_favourite_meal(item)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.delete("/delete", status_code=status.HTTP_200_OK)
def remove_meal(item: uuid.UUID, service: UserFavouriteMealService = Depends(get_service)):
    try:
        service.remove_user_favourite_meal(item)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.get("/user-id", response_model=list[UserFavouriteMealResponseDTO], status_code=status.HTTP_200_OK)
def get_user_favourite_meals_by_user_id(user_id: uuid.UUID, service: UserFavouriteMealService = Depends(get_service)):
    try:
        return service.get_user_favourite_meal_by_user_id(user_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))