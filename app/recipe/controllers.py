from fastapi import APIRouter
import recipe.services as service
from handle.response import response
from handle.exception import exception

router = APIRouter()

@router.delete('/recipe/{menu}/{ingredient}')
async def delete (menu: str, ingredient: str):
    try:
        recipe = await service.delete_recipe(menu, ingredient)
        return response(recipe)

    except Exception as e:
        return exception(500, e)