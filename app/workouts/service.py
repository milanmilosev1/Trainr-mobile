import uuid
from datetime import datetime, timezone

from app.workouts.models import Workout
from app.workouts.repository import WorkoutRepository
from app.workouts.schemas import CreateWorkoutDTO, UpdateWorkoutDTO


class WorkoutService:
    def __init__(self, repo: WorkoutRepository):
        self.repo = repo

    def create_new_workout(self, new_workout: CreateWorkoutDTO) -> Workout:
        workout = Workout(
            id = uuid.uuid4(),
            user_id = new_workout.user_id,
            date = new_workout.date,
            name = new_workout.name,
            notes = new_workout.notes,
            is_completed = new_workout.is_completed,
            created_at = datetime.now(timezone.utc)
        )

        return self.repo.add(workout)

    def delete_workout(self, workout_id: uuid.UUID) -> None:
        found = self.repo.get_by_id(workout_id)
        if found is None:
            raise KeyError("Workout not found")

        self.repo.remove(found)

    def get_workout_by_id(self, workout_id) -> Workout | None:
        return self.repo.get_by_id(workout_id)

    def get_all_workouts(self) -> list[Workout]:
        return self.repo.get_all()

    def update_workout_info(self, new_workout: UpdateWorkoutDTO) -> Workout:
        found = self.repo.get_by_id(new_workout.id)

        if found is None:
            raise KeyError("Meal does not exist")

        return self.repo.update(found, new_workout)