from pydantic import BaseModel
from datetime import datetime


class Event(BaseModel):
    title: str
    date: datetime
    location: str | None
    url: str
    source: str
