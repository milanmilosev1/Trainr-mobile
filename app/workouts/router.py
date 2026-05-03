from http.client import HTTPException
import uuid

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.workouts.models import Workout
from app.workouts.repository import WorkoutRepository
from app.workouts.schemas import UpdateWorkoutDTO, WorkoutResponseDTO, CreateWorkoutDTO
from app.workouts.service import WorkoutService

router = APIRouter(prefix="/workouts", tags=["Workouts"])

def get_workout_service(db: Session = Depends(get_db)) -> WorkoutService:
    repo = WorkoutRepository(db)
    return WorkoutService(repo)

@router.get("/all", response_model=list[WorkoutResponseDTO], status_code=status.HTTP_200_OK)
def get_all_workouts(service: WorkoutService = Depends(get_workout_service)) -> list[Workout]:
    try:
        return service.get_all_workouts()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.get("/id", response_model=WorkoutResponseDTO, status_code=status.HTTP_200_OK)
def get_workout_by_id(workout_id: uuid.UUID, service: WorkoutService = Depends(get_workout_service)) -> Workout | None:
    try:
        workout = service.get_workout_by_id(workout_id)
        if workout is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Workout with the id: {workout_id} is not found!")

        return workout
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.post("/", response_model=WorkoutResponseDTO, status_code=status.HTTP_200_OK)
def add_new_workout(new_workout: CreateWorkoutDTO, service: WorkoutService = Depends(get_workout_service)) -> Workout:
    try:
        return service.create_new_workout(new_workout)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.patch("/update", response_model=WorkoutResponseDTO, status_code=status.HTTP_200_OK)
def update_workout_info(new_workout: UpdateWorkoutDTO, service: WorkoutService = Depends(get_workout_service)) -> Workout:
    try:
        return service.update_workout_info(new_workout)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

@router.delete("/id", response_model=None, status_code=status.HTTP_200_OK)
def remove_workout(workout_id: uuid.UUID, service: WorkoutService = Depends(get_workout_service)) -> None:
    try:
        return service.delete_workout(workout_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))