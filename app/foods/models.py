import uuid

from sqlalchemy.orm import Mapped, mapped_column

from app.db import db_connection

Base = db_connection.Base

class Food(Base):
    __tablename__ = "foods"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    calories_per_serving: Mapped[int] = mapped_column(nullable=False)
    protein_g: Mapped[int] = mapped_column(nullable=False)
    carbs_g: Mapped[int] = mapped_column(nullable=False)
    fat_g: Mapped[int] = mapped_column(nullable=False)
    serving_size: Mapped[str] = mapped_column(nullable=False)