from fastapi import APIRouter
import ingredient.services as service
from handle.response import response
from handle.exception import exception
from prisma.errors import UniqueViolationError
from ingredient.models import CreateIngredient, UpdateIngredient

router = APIRouter()

@router.get('/shop/{id}/ingredient')
async def get (id: str):
    try:
        ingredient = await service.get_ingredients(id)
        return response(ingredient)

    except Exception as e:
        return exception(500, e)

@router.get('/shop/{id}/ingredient/search')
async def search (id: str, key: str):
    try:
        fetch = await service.find_ingredient(id, key)
        return response(fetch)

    except Exception as e:
        return exception(500, e)

@router.post('/ingredient')
async def create (body: CreateIngredient):
    try:
        ingredient = await service.create_ingredient(body)
        return response(ingredient)

    except UniqueViolationError as e:
        return exception(400)

    except Exception as e:
        return exception(500, e)

@router.patch('/ingredient/{id}')
async def update (body: UpdateIngredient, id: str):
    try:
        ingredient = await service.update_ingredient(body, id)
        return response(ingredient)

    except Exception as e:
        return exception(500, e)

@router.delete('/ingredient/{id}')
async def delete (id: str):
    try:
        ingredient = await service.delete_ingredient(id)
        return response(ingredient)

    except Exception as e:
        return exception(500, e)