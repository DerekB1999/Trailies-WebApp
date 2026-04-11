from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel
from schemas import Difficulty


class User(SQLModel, table=True):
    user_id: int | None = Field(default=None, primary_key=True)
    first_name: str = Field(..., min_length=1, max_length=25)
    last_name: str = Field(..., min_length=1, max_length=25)
    username: str = Field(..., min_length=5, max_length=25)
    email: str = Field(..., max_length=254)
    hashed_password: str
    role: str = Field(default='user')


class Trail(SQLModel, table=True):
    # int | None because before we have a trail in the database, trail_id is None
    trail_id: int | None = Field(default=None, primary_key=True)
    # ... indicates no default value, therefore required
    name: str = Field(..., min_length=1, max_length=50)
    distance: float = Field(..., ge=1, le=50)
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    alt: float | None = None
    surface: str = Field(..., min_length=1, max_length=25)
    difficulty: Difficulty = Field(...)
    bike_friendly: bool = Field(...)
    dog_friendly: bool = Field(...)
    description: Optional[str] = Field(
        default=None, min_length=0, max_length=500)


class TrailReview(SQLModel, table=True):
    review_id: int | None = Field(default=None, primary_key=True)
    trail_id: int = Field(foreign_key='trail.trail_id')
    user_id: int = Field(foreign_key='user.user_id')
    rating: float = Field(..., ge=0, le=5)
    comment: Optional[str] = Field(default=None, min_length=0, max_length=500)
    # Without default_factory=lambda: , every new trailReview will share the same timestamp
    # timezone.utc makes datetime timezone aware
    # .utc sets the datetime to Coordinated Universal Time(UTC)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
