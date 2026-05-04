import uuid

from app.foods.models import Food
from app.foods.repository import FoodRepository
from app.foods.schemas import CreateFoodDTO, UpdateFoodDTO


class FoodService:
    def __init__(self, repo: FoodRepository):
        self.repo = repo

    def create_new_food(self, new_food: CreateFoodDTO) -> Food:
        food = Food(
            id = uuid.uuid4(),
            name = new_food.name,
            calories_per_serving = new_food.calories_per_serving,
            protein_g = new_food.protein_g,
            carbs_g = new_food.carbs_g,
            fat_g = new_food.fat_g,
            serving_size = new_food.serving_size
        )

        return self.repo.add(food)

    def remove_food(self, food_id: uuid.UUID) -> None:
        existing = self.repo.get_by_id(food_id)

        if existing is None:
            raise KeyError(f"Exercise with id: {food_id} does not exist")

        self.repo.remove(existing)

    def update_food_info(self, food: UpdateFoodDTO) -> Food:
        found = self.repo.get_by_id(food.id)

        if found is None:
            raise KeyError("Food does not exist")

        return self.repo.update(found, food)

    def get_all_foods(self) -> list[Food]:
        return self.repo.get_all()

    def get_food_by_id(self, food_id) -> Food | None:
        return self.repo.get_by_id(food_id)