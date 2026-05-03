import uuid

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.db_connection import get_db
from app.exercises.repository import ExerciseRepository
from app.exercises.service import ExerciseService
from app.exercises.schemas import CreateExerciseDTO, ExerciseResponseDTO, UpdateExerciseDTO

router = APIRouter(prefix="/exercises", tags=["Exercises"])

def get_exercise_service(db: Session = Depends(get_db)):
    repo = ExerciseRepository(db)
    return ExerciseService(repo)

@router.get("/", response_model=list[ExerciseResponseDTO], status_code=status.HTTP_200_OK)
def get_all_exercises(service: ExerciseService = Depends(get_exercise_service)):
    try:
        return service.get_all_exercises()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error:\nDetails: {error}")
    
@router.get("/id", response_model=ExerciseResponseDTO, status_code=status.HTTP_200_OK)
def get_exercise_by_id(exercise_id: uuid.UUID, service: ExerciseService = Depends(get_exercise_service)):
    try:
        exercise = service.get_exercise_by_id(exercise_id)
        if exercise is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exercise with id: {exercise_id} not found!")
        
        return exercise
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error:\nDetails: {error}")
    
@router.post("/", response_model=ExerciseResponseDTO, status_code=status.HTTP_200_OK)
def add_exercise(exercise: CreateExerciseDTO, service: ExerciseService = Depends(get_exercise_service)):
    try:
        return service.create_new_exercise(exercise)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error:\nDetails: {error}")
    
@router.patch("/update", response_model=ExerciseResponseDTO, status_code=status.HTTP_200_OK)
def update_exercise(new_exercise: UpdateExerciseDTO, service: ExerciseService = Depends(get_exercise_service)):
    try:
        return service.update_exercise_info(new_exercise)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exercise with id: {new_exercise.id} not found!")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error:\nDetails: {error}")

@router.delete("/delete", status_code=status.HTTP_200_OK)
def remove_exercise(exercise_id: uuid.UUID, service: ExerciseService = Depends(get_exercise_service)):
    try:
        service.remove_exercise(exercise_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Exercise with id: {exercise_id} not found!")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error:\nDetails: {error}")
