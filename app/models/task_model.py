from sqlalchemy import Boolean, Integer, String, text, Identity
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=False),
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(String(100), nullable=False)

    completed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )

    age: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("18"))

    status: Mapped[str]     = mapped_column(
        String(20), nullable=False, server_default=text("pending")
    )
