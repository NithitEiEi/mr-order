from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class CreateItem(BaseModel):
    item: str
    name: str
    quantity: int

class UpdateItem(BaseModel):
    item: Optional[str] = None
    name: Optional[str] = None
    quantity: Optional[int] = None

class CreateReceipt(BaseModel):
    date: Optional[datetime] = None
    total: float
    shop: str
    detail: list[CreateItem]

class UpdateReceipt(BaseModel):
    date: Optional[datetime] = None
    total: Optional[float] = None
    detail: Optional[list[UpdateItem]] = None