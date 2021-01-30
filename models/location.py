from typing import Optional

from pydantic import BaseModel


class Location(BaseModel):
    city: str
    country: Optional[str] = 'UK'
    state: Optional[str] = None

