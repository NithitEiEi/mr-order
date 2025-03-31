from pydantic import BaseModel
from typing import Optional

class CreateShop(BaseModel):
    user: str
    name: str
    account: Optional[str] = None
    account_eng: Optional[str] = None

class UpdateShop(BaseModel):
    name: Optional[str] = None
    open: Optional[bool] = None
    account: Optional[str] = None
    account_eng: Optional[str] = None