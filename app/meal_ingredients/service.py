import uuid

from app.meal_ingredients.models import MealIngredient
from app.meal_ingredients.repository import MealIngredientRepository
from app.meal_ingredients.schemas import CreateMealIngredientDTO, UpdateMealIngredientDTO


class MealIngredientService:
    def __init__(self, repo: MealIngredientRepository):
        self.repo = repo

    def create_new_meal_ingredient(self, ingredient: CreateMealIngredientDTO) -> MealIngredient | None:
        new = MealIngredient(
            id = uuid.uuid4(),
            meal_id = ingredient.meal_id,
            food_id = ingredient.food_id,
            quantity = ingredient.quantity
        )

        return self.repo.add(new)

    def get_meal_ingredient_by_id(self, mi_id: uuid.UUID) -> MealIngredient | None:
        found = self.repo.get_by_id(mi_id)
        if found is None:
            raise KeyError("Meal ingredient not found")

        return found

    def get_all_meal_ingredients(self) -> list[MealIngredient]:
        return self.repo.get_all()

    def remove_meal_ingredient(self, mi_id) -> None:
        found = self.repo.get_by_id(mi_id)
        if found is None:
            raise KeyError("Meal ingredient not found")

        self.repo.remove(found)

    def update_meal_ingredient_info(self, dto: UpdateMealIngredientDTO) -> MealIngredient:
        found = self.repo.get_by_id(dto.id)
        if found is None:
            raise KeyError("Meal ingredient not found")

        return self.repo.update(found, dto)
