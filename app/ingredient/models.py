from pydantic import BaseModel
from typing import Optional

class CreateIngredient(BaseModel):
    name: str
    unit: str
    ages: int
    ages_unit: str
    shop: str


class UpdateIngredient(BaseModel):
    name: Optional[str] = None
    unit: Optional[str] = None
    ages: Optional[int] = None
    ages_unit: Optional[str] = None