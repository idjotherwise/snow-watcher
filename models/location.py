from typing import Optional

from pydantic import BaseModel


class Location(BaseModel):
    city: str
    country: Optional[str] = 'GB'
    state: Optional[str] = None

