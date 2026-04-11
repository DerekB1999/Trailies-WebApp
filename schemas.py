from enum import Enum
from typing import Annotated, Optional

from pydantic import BaseModel, Field, StringConstraints


# Difficulties for Trails table
class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


# Password for user tables
Password = Annotated[str, StringConstraints(
    min_length=8, max_length=64, pattern=r"^[!-~]+$"
)]


# Location of trails
class GeoPoint(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    alt: Optional[float] = None
