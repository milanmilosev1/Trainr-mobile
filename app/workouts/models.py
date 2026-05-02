import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column

from app.db import db_connection

Base = db_connection.Base

class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default= uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column()
    date: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    name: Mapped[str] = mapped_column()
    notes: Mapped[str] = mapped_column()
    is_completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
