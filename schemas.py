# define what to accept and return from API
from __future__ import annotations

from datetime import UTC, date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=100)


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True) # allow pydantic read from SQLAlchemy model

    id: int # id is not included model_config
    username: str

class UserPrivate(UserPublic):
    email: EmailStr


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=100)

class Token(BaseModel):
    access_token: str
    token_type: str


class ReviewBase(BaseModel):
    restaurant_name: str = Field(min_length=1, max_length=100)
    review: str | None = Field(default=None, min_length=1, max_length=500)
    date_visited: date | None = Field(default_factory=lambda: datetime.now(UTC).date())


class ReviewCreate(ReviewBase):
    pass
    

class ReviewUpdate(BaseModel):
    restaurant_name: str | None = Field(default=None, min_length=1, max_length=100)
    review: str | None = Field(default=None, min_length=1, max_length=500)
    date_visited: date | None = Field(default_factory=lambda: datetime.now(UTC).date())

class ReviewResponse(ReviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    reviewer: UserPublic

