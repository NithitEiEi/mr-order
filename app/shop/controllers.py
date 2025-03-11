from fastapi import APIRouter
import shop.services as services
from handle.response import response
from handle.exception import exception
from shop.models import CreateShop, UpdateShop
from prisma.errors import UniqueViolationError

router = APIRouter()

@router.get('/shop/{id}')
async def get (id: str):
    try:
        shop = await services.get_shop(id)
        return response(shop)

    except AttributeError as e:
        return exception(404)

    except Exception as e:
        return exception(500, e)

@router.post('/shop')
async def post (body: CreateShop):
    try:
        shop = await services.create_shop(body)
        return response(shop)

    except UniqueViolationError:
        return exception(400)

    except Exception as e:
        return exception(500, e)

@router.patch('/shop/{id}')
async def update (body: UpdateShop, id: str):
    try:
        shop = await services.update_shop(body, id)
        return response(shop)

    except AttributeError as e:
        return exception(404)

    except Exception as e:
        return exception(500, e)

@router.delete('/shop/{id}')
async def update (id: str):
    try:
        shop = await services.delete_shop(id)
        return response(shop)

    except AttributeError as e:
        return exception(404)

    except Exception as e:
        return exception(500, e)