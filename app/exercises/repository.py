from datetime import datetime, timezone
import uuid

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.exercises.models import Exercise

class ExerciseRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Exercise]:
        return self.session.query(Exercise).all()

    def get_by_id(self, exercise_id: uuid.UUID) -> Exercise | None:
        return self.session.get(Exercise, exercise_id)

    def add(self, exercise: Exercise) -> Exercise | None:
        try:
            self.session.add(exercise)
            self.session.commit()
            self.session.refresh(exercise)
            return exercise
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def remove(self, exercise: Exercise) -> None:
        try:
            self.session.delete(exercise)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def update(self, found: Exercise, new: Exercise) -> Exercise:
        try:
            data = new.model_dump(exclude_unset=True)

            for key, value in data.items():
                if key != "id":
                    setattr(found, key, value)

            self.session.commit()
            self.session.refresh(found)

            return found

        except SQLAlchemyError:
            self.session.rollback()
            raise
