import uuid

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.user_meal_plans.models import UserMealPlan
from app.user_meal_plans.schemas import UpdateUserMealPlanDTO


class UserMealPlanRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, user_meal_plan: UserMealPlan) -> UserMealPlan | None:
        try:
            self.session.add(user_meal_plan)
            self.session.commit()
            self.session.refresh(user_meal_plan)
            return user_meal_plan
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def remove(self, user_meal_plan: UserMealPlan) -> None:
        try:
            self.session.delete(user_meal_plan)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get_by_id(self, ump_id: uuid.UUID) -> UserMealPlan | None:
        return self.session.get(UserMealPlan, ump_id)

    def get_all(self) -> list[UserMealPlan]:
        return self.session.query(UserMealPlan).all()

    def get_by_user_id(self, user_id) -> list[UserMealPlan]:
        return self.session.query(UserMealPlan).where(UserMealPlan.user_id == user_id).all()

    def update(self, found: UserMealPlan, dto: UpdateUserMealPlanDTO):
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