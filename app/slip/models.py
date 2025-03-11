from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class SlipStatus (str, Enum):
    valid = "VALID"
    invalid = "INVALID"
    no_slip = "NO_SLIP"


class WebhookSlip (BaseModel):
    customer: str
    image: str

class CreateSlip (BaseModel):
    sender: str
    receiver: str
    amount: float
    date: datetime
    status: Optional[SlipStatus] = None
    ref: str
    order: str