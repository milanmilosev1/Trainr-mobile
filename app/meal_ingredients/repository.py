import uuid

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.meal_ingredients.models import MealIngredient
from app.meal_ingredients.schemas import UpdateMealIngredientDTO


class MealIngredientRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, meal_ingredient: MealIngredient) -> MealIngredient | None:
        try:
            self.session.add(meal_ingredient)
            self.session.commit()
            self.session.refresh(meal_ingredient)
            return meal_ingredient
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def remove(self, meal_ingredient: MealIngredient) -> None:
        try:
            self.session.delete(meal_ingredient)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get_by_id(self, meal_ingredient_id: uuid.UUID) -> MealIngredient | None:
        return self.session.get(MealIngredient, meal_ingredient_id  )

    def get_all(self) -> list[MealIngredient]:
        return self.session.query(MealIngredient).all()

    def update(self, found: MealIngredient, dto: UpdateMealIngredientDTO) -> MealIngredient:
        try:
            data = dto.model_dump(exclude_unset=True)

            for key, value in data.items():
                if key != "id":
                    setattr(found, key, value)

            self.session.commit()
            self.session.refresh(found)

            return found

        except SQLAlchemyError:
            self.session.rollback()
            raise