from typing import Optional
from pydantic import BaseModel

class CreateRecipe(BaseModel):
    ingredient: str
    amount: float

class UpdateRecipe(BaseModel):
    ingredient: str
    amount: Optional[float] = None