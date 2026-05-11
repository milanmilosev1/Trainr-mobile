import uuid

from sqlalchemy.orm import Mapped, mapped_column

from app.db import db_connection

Base = db_connection.Base

class ShoppingListItem(Base):
    __tablename__ = "shopping_list_items"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    shopping_list_id: Mapped[uuid.UUID] = mapped_column()
    ingredient_name: Mapped[str] = mapped_column()
    is_checked: Mapped[bool] = mapped_column(default=False)
    quantity: Mapped[int] = mapped_column()