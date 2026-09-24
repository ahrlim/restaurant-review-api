# Define what we store in the database

from __future__ import annotations

from datetime import UTC, datetime
from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    reviews: Mapped[list[Review]] = relationship(
        back_populates="reviewer",
        cascade="all, delete-orphan",
    )


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "restaurant_name",
            name="uq_reviews_user_restaurant",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    restaurant_name: Mapped[str] = mapped_column(String(100), nullable=False)
    review: Mapped[str | None] = mapped_column(String(500))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    date_visited: Mapped[datetime | None] = mapped_column(default=lambda: datetime.now(UTC))

    reviewer: Mapped[User] = relationship(back_populates="reviews")