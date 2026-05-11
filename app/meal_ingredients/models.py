import uuid

from sqlalchemy.orm import Mapped, mapped_column

from app.db import db_connection

Base = db_connection.Base

class MealIngredient(Base):
    __tablename__ = "meal_ingredients"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    meal_id: Mapped[uuid.UUID] = mapped_column()
    food_id: Mapped[uuid.UUID] = mapped_column()
    quantity: Mapped[int] = mapped_column()