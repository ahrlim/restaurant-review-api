# define what to accept and return from API
from __future__ import annotations

from datetime import datetime

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True) # allow pydantic read from SQLAlchemy model

    id: int # id is not included model_config


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)


class RestaurantBase(BaseModel):
    restaurant_name: str = Field(min_length=1, max_length=50)
    neighborhood: str | None = Field(default=None, min_length=1, max_length=50)
    

class RestaurantCreate(RestaurantBase):
    date_added: datetime = Field(default_factory=datetime.now)


class RestaurantUpdate(BaseModel):
    restaurant_name: str | None = Field(default=None, min_length=1, max_length=50)
    neighborhood: str | None = Field(default=None, min_length=1, max_length=50)


class RestaurantResponse(RestaurantBase):
    model_config = ConfigDict(from_attributes=True)

    date_added: datetime
    id: int
    visits: list[VisitResponse]


class VisitCreate(BaseModel):
    date_visited: datetime | None = Field(default=None)


class VisitUpdate(BaseModel):
    restaurant_id: int | None = Field(default=None)
    date_visited: datetime | None = Field(default=None)


class VisitResponse(VisitCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    restaurant_id: int
    review: ReviewResponse | None


class ReviewCreate(BaseModel):
    rating: float = Field(default=0, ge=0, le=10)
    notes: str | None = Field(default=None, min_length=1, max_length=500)


class ReviewUpdate(BaseModel):
    # Will not allow to change visit_id
    rating: float | None = Field(default=None, ge=0, le=10)
    notes: str | None = Field(default=None, min_length=1, max_length=500)


class ReviewResponse(ReviewCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    visit_id: int

