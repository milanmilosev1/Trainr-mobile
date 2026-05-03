import uuid

from app.db import db_connection
from sqlalchemy.orm import Mapped, mapped_column

Base = db_connection.Base

class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    muscle_group: Mapped[str] = mapped_column()
    equipment_type: Mapped[str] = mapped_column()