import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column

from app.db import db_connection
from app.meals.models import MealType

Base = db_connection.Base

class UserMealPlan(Base):
    __tablename__ = "user_meal_plans"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column()
    date: Mapped[datetime] = mapped_column()
    meal_id: Mapped[uuid.UUID] = mapped_column()
    meal_slot: Mapped[MealType] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))