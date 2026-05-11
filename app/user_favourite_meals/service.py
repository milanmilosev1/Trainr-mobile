import uuid
from datetime import datetime, timezone

from app.user_favourite_meals.models import UserFavouriteMeal
from app.user_favourite_meals.repository import UserFavouriteMealRepository
from app.user_favourite_meals.schemas import CreateUserFavouriteMealDTO, UpdateUserFavouriteMealDTO


class UserFavouriteMealService:
    def __init__(self, repo: UserFavouriteMealRepository):
        self.repo = repo

    def create_user_favourite_meal(self, new: CreateUserFavouriteMealDTO) -> UserFavouriteMeal:
        meal = UserFavouriteMeal(
            id = uuid.uuid4(),
            user_id = new.user_id,
            meal_id = new.meal_id,
            created_at = datetime.now(timezone.utc)
        )

        return self.repo.add(meal)

    def get_user_favourite_meal_by_id(self, ufm_id: uuid.UUID) -> UserFavouriteMeal:
        found = self.repo.get_by_id(ufm_id)
        if found is None:
            raise KeyError("Meal not found")

        return found

    def get_all_user_favourite_meals(self) -> list[UserFavouriteMeal]:
        return self.repo.get_all()

    def get_user_favourite_meal_by_user_id(self, user_id: uuid.UUID) -> list[UserFavouriteMeal]:
        return [x for x in self.repo.get_all() if x.user_id == user_id]

    def remove_user_favourite_meal(self, ufm_id: uuid.UUID) -> None:
        found = self.repo.get_by_id(ufm_id)
        if found is None:
            raise KeyError("Meal not found")

        self.repo.remove(found)

    def update_user_favourite_meal(self, updated: UpdateUserFavouriteMealDTO) -> UserFavouriteMeal:
        found = self.repo.get_by_id(updated.id)
        if found is None:
            raise KeyError("Meal not found")

        return self.repo.update(found, updated)

