from typing import Optional
from pydantic import BaseModel
from recipe.models import CreateRecipe, UpdateRecipe

class CreateMenu(BaseModel):
    name: str
    price: float
    shop: str
    recipe: Optional[list[CreateRecipe]] = None

class UpdateMenu(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    recipe: Optional[list[UpdateRecipe]] = None