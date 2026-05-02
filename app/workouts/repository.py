import uuid
from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.workouts.models import Workout
from app.workouts.schemas import UpdateWorkoutDTO


class WorkoutRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, workout: Workout) -> Workout:
        try:
            self.session.add(workout)
            self.session.commit()
            self.session.refresh(workout)
            return workout
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def remove(self, workout: Workout) -> None:
        try:
            self.session.delete(workout)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def update(self, workout: Workout, dto: UpdateWorkoutDTO) -> Workout:
        try:
            data = dto.model_dump(exclude_unset=True)

            for key, value in data.items():
                if key != "id":
                    setattr(workout, key, value)

            self.session.commit()
            self.session.refresh(workout)

            return workout

        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get_by_id(self, workout_id: uuid.UUID) -> Workout | None:
        return self.session.get(Workout, workout_id)

    def get_all(self) -> list[Workout]:
        return self.session.query(Workout).all()

    def get_by_name(self, workout_name: str) -> list[Workout] | None:
        return self.session.query(Workout).where(Workout.name == workout_name).all()
