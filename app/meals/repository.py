from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.meals.models import Meal
from app.meals.schemas import UpdateMealDTO


class MealRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, meal_id: UUID) -> Meal | None:
        return self.session.get(Meal, meal_id)

    def get_all(self) -> list[Meal]:
        return self.session.query(Meal).all()

    def get_by_name(self, meal_name: str) -> Meal | None:
        return self.session.query(Meal).where(Meal.name == meal_name).first()

    def add(self, meal: Meal) -> Meal:
        try:
            self.session.add(meal)
            self.session.commit()
            self.session.refresh(meal)
            return meal
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def remove(self, meal: Meal) -> None:
        try:
            self.session.delete(meal)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def update(self, found: Meal, dto: UpdateMealDTO) -> Meal:
        try:
            data = dto.model_dump(exclude_unset=True)

            for key, value in data.items():
                if key != "id":
                    setattr(found, key, value)

            found.updated_at = datetime.now(timezone.utc)

            self.session.commit()
            self.session.refresh(found)

            return found

        except SQLAlchemyError:
            self.session.rollback()
            raise