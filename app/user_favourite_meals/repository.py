import uuid

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.user_favourite_meals.models import UserFavouriteMeal
from app.user_favourite_meals.schemas import UpdateUserFavouriteMealDTO


class UserFavouriteMealRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, user_favourite_meal: UserFavouriteMeal) -> UserFavouriteMeal | None:
        try:
            self.session.add(user_favourite_meal)
            self.session.commit()
            self.session.refresh(user_favourite_meal)
            return user_favourite_meal
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def remove(self, user_favourite_meal: UserFavouriteMeal) -> None:
        try:
            self.session.delete(user_favourite_meal)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def get_by_id(self, ufm_id: uuid.UUID) -> UserFavouriteMeal | None:
        return self.session.get(UserFavouriteMeal, ufm_id)

    def get_all(self) -> list[UserFavouriteMeal]:
        return self.session.query(UserFavouriteMeal).all()

    def update(self, old: UserFavouriteMeal, new: UpdateUserFavouriteMealDTO) -> UserFavouriteMeal:
        try:
            data = new.model_dump(exclude_unset=True)

            for key, value in data.items():
                if key != "id":
                    setattr(old, key, value)

            self.session.commit()
            self.session.refresh(old)

            return old

        except SQLAlchemyError:
            self.session.rollback()
            raise

