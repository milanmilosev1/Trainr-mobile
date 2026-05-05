import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import mapped_column, Mapped

from app.db import db_connection

Base = db_connection.Base

class UserShoppingList(Base):
    __tablename__ = "user_shopping_lists"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column()
    start_date: Mapped[datetime] = mapped_column()
    end_date: Mapped[datetime] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))