import uuid

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.foods.models import Food
from app.foods.schemas import UpdateFoodDTO


class FoodRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, food_id: uuid.UUID) -> Food | None:
        return self.session.get(Food, food_id)

    def get_all(self) -> list[Food]:
        return self.session.query(Food).all()

    def add(self, food: Food) -> Food:
        try:
            self.session.add(food)
            self.session.commit()
            self.session.refresh(food)
            return food
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def remove(self, food: Food) -> None:
        try:
            self.session.delete(food)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def update(self, found: Food, new: UpdateFoodDTO) -> Food:
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