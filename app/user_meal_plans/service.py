import uuid
from datetime import datetime, timezone

from app.user_meal_plans.models import UserMealPlan
from app.user_meal_plans.repository import UserMealPlanRepository
from app.user_meal_plans.schemas import CreateUserMealPlanDTO, UpdateUserMealPlanDTO


class UserMealPlanService:
    def __init__(self, repo: UserMealPlanRepository):
        self.repo = repo

    def create_new_user_meal_plan(self, dto: CreateUserMealPlanDTO) -> UserMealPlan | None:
        new = UserMealPlan(
            id = uuid.uuid4(),
            user_id = dto.user_id,
            date = dto.date,
            meal_id = dto.meal_id,
            meal_slot = dto.meal_slot,
            created_at = datetime.now(timezone.utc)
        )

        return self.repo.add(new)

    def get_user_meal_plan_by_id(self, user_meal_plan_id: uuid.UUID) -> UserMealPlan:
        found = self.repo.get_by_id(user_meal_plan_id)
        if found is None:
            raise KeyError("This meal plan does not exist")

        return found

    def get_user_meal_plan_by_user_id(self, user_id: uuid.UUID) -> list[UserMealPlan]:
        found = self.repo.get_by_user_id(user_id)
        if found is None:
            raise KeyError("This user does not have any meal plans")

        return found

    def get_all_user_meal_plans(self) -> list[UserMealPlan]:
        return self.repo.get_all()

    def update_user_meal_plan_info(self, updated: UpdateUserMealPlanDTO) -> UserMealPlan:
        found = self.repo.get_by_id(updated.id)

        if found is None:
            raise KeyError("User meal plan does not exist")

        return self.repo.update(found, updated)

    def remove_user_meal_plan(self, user_meal_plan_id: uuid.UUID) -> None:
        found = self.repo.get_by_id(user_meal_plan_id)
        if found is None:
            raise KeyError("User meal plan does not exist")

        self.repo.remove(found)