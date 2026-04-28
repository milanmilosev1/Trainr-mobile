from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db import db_connection

from enum import Enum

class MealType(Enum):
    breakfast = 1
    lunch = 2
    dinner = 3
    snack = 4

class MealDifficulty(Enum):
    easy = 1
    medium = 2
    hard = 3

Base = db_connection.Base

class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    meal_type: Mapped[MealType] = mapped_column()
    calories: Mapped[int] = mapped_column()
    protein_g: Mapped[int] = mapped_column()
    carbs_g: Mapped[int] = mapped_column()
    fat_g: Mapped[int] = mapped_column()
    cook_time_minutes: Mapped[int] = mapped_column()
    difficulty: Mapped[MealDifficulty] = mapped_column()
    tags: Mapped[list[str]] = mapped_column(JSONB, default=list)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
