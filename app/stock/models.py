from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CreateStock(BaseModel):
    remain: float
    ingredient: str

class UpdateStock(BaseModel):
    add_date: Optional[datetime] = None
    expire: Optional[datetime] = None
    remain: Optional[int] = None