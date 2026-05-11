import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column

from app.db import db_connection

Base = db_connection.Base

class UserFavouriteMeal(Base):
    __tablename__ = "user_favourite_meals"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column()
    meal_id: Mapped[uuid.UUID] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))