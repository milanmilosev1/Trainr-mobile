import uuid
from _pyrepl import keymap
from datetime import datetime, timezone

from app.meals.models import Meal
from app.meals.repository import MealRepository
from app.meals.schemas import CreateMealDTO


class MealService:
    def __init__(self, repo: MealRepository):
        self.repo = repo

    def create_new_meal(self, new_meal: CreateMealDTO) -> Meal:
        meal = Meal(
            id=uuid.uuid4(),
            name=new_meal.name,
            meal_type=new_meal.meal_type,
            calories=new_meal.calories,
            protein_g=new_meal.protein_g,
            carbs_g=new_meal.carbs_g,
            fat_g=new_meal.fat_g,
            cook_time_minutes=new_meal.cook_time_minutes,
            difficulty=new_meal.difficulty,
            tags=new_meal.tags,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        return self.repo.add(meal)

    def delete_meal(self, meal_id: uuid.UUID) -> None:
        existing = self.repo.get_by_id(meal_id)

        if existing is None:
            raise KeyError("Meal does not exist")

        self.repo.remove(existing)

    def update_meal(self, meal: Meal) -> Meal:
       success = self.repo.update(meal)

       if success is None:
           raise KeyError("Error updating meal")

       return success

    def get_all_meals(self):
        return self.repo.get_all()

    def get_meal_by_id(self, meal_id):
        return self.repo.get_by_id(meal_id)