# define what to accept and return from API
from __future__ import annotations

from datetime import datetime

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



class ReviewBase(BaseModel):
    restaurant_name: str = Field(min_length=1, max_length=100)
    review: str | None = Field(default=None, min_length=1, max_length=500)
    date_visited: datetime | None = Field(default_factory=datetime.now)


class ReviewCreate(ReviewBase):
    user_id: int = Field(gt=0)  # reviewer_id must be greater than 0
    

class ReviewUpdate(BaseModel):
    restaurant_name: str | None = Field(default=None, min_length=1, max_length=100)
    review: str | None = Field(default=None, min_length=1, max_length=500)
    date_visited: datetime | None = Field(default_factory=datetime.now)

class ReviewResponse(ReviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    reviewer: UserResponse

