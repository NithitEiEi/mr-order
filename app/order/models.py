from enum import Enum
from typing import Optional
from pydantic import BaseModel

class Payment(str, Enum):
    cash = "CASH"
    transfer = "TRANSFER"

class OrderProcess(str, Enum):
    pending = "PENDING"
    done = "DONE"
    complete = "COMPLETE"
    cancel = "CANCEL"

class CreateDetail(BaseModel):
    menu: str
    amount: int

class UpdateDetail(BaseModel):
    menu: Optional[str] = None
    amount: Optional[int] = None

class CreateOrder(BaseModel):
    customer: str
    shop: str
    payment: Optional[Payment] = None
    address: Optional[str] = None
    total: float
    detail: list[CreateDetail]

class UpdateOrder(BaseModel):
    payment: Optional[Payment] = None
    address: Optional[str] = None
    process: Optional[OrderProcess] = None
    total: Optional[float] = None
    detail: Optional[list[CreateDetail]] = None