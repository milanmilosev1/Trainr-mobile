from http.client import HTTPException

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.util import string_or_unprintable

from app.db.db_connection import get_db
from app.workouts.models import Workout
from app.workouts.repository import WorkoutRepository
from app.workouts.schemas import WorkoutResponseDTO, CreateWorkoutDTO
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

@router.post("/", response_model=WorkoutResponseDTO, status_code=status.HTTP_200_OK)
def add_new_workout(new_workout: CreateWorkoutDTO, service: WorkoutService = Depends(get_workout_service)) -> Workout:
    try:
        return service.create_new_workout(new_workout)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error))

