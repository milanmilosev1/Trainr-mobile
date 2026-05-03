import uuid

from app.exercises.repository import ExerciseRepository
from app.exercises.schemas import CreateExerciseDTO, UpdateExerciseDTO
from app.exercises.models import Exercise

class ExerciseService:
    def __init__(self, repo: ExerciseRepository):
        self.repo = repo

    def create_new_exercise(self, new_exercise: CreateExerciseDTO) -> Exercise | None:
        exercise = Exercise(
            id = uuid.uuid4(),
            name = new_exercise.name,
            description = new_exercise.description,
            muscle_group = new_exercise.muscle_group,
            equipment_type = new_exercise.equipment_type
        )

        return self.repo.add(exercise)
    
    def remove_exercise(self, exercise_id: uuid.UUID) -> None:
        existing = self.repo.get_by_id(exercise_id)

        if existing is None:
            raise KeyError(f"Exercise with id: {exercise_id} does not exist")
        
        self.repo.remove(existing)

    def update_exercise_info(self, exercise: UpdateExerciseDTO) -> Exercise:
        found = self.repo.get_by_id(exercise.id)

        if found is None:
            raise KeyError("Meal does not exist")

        return self.repo.update(found, exercise)
    
    def get_all_exercises(self) -> list[Exercise]:
        return self.repo.get_all()

    def get_exercise_by_id(self, exercise_id) -> Exercise:
        return self.repo.get_by_id(exercise_id)