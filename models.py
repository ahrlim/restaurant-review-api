# Define what we store in the database

from __future__ import annotations

from datetime import UTC, datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class Restaurant(Base): # restaurant the user saved
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    restaurant_name: Mapped[str] = mapped_column(String(50), nullable=False)
    neighborhood: Mapped[str | None] = mapped_column(String(50))
    date_added: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )
    visits: Mapped[list[Visit]] = relationship(back_populates="restaurant")


class Visit(Base):  # keep a record if the user visited or not
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date_visited: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
    )
    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurants.id"),
        nullable=False,
        index=True,
    )
    restaurant: Mapped[Restaurant] = relationship(back_populates="visits")
    review: Mapped[Review] = relationship(back_populates="visit")

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    notes: Mapped[str | None] = mapped_column(String(500))
    visit_id: Mapped[int] = mapped_column(
        ForeignKey("visits.id"),
        nullable=False,
        index=True,
        unique=True,
    )   
    visit: Mapped[Visit] = relationship(back_populates="review")
