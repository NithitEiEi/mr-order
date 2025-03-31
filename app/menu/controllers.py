from fastapi import APIRouter
import menu.services as service
from handle.response import response
from handle.exception import exception
from prisma.errors import UniqueViolationError
from menu.models import CreateMenu, UpdateMenu

router = APIRouter()

@router.get('/shop/{id}/menu')
async def get (id: str):
    try:
        menus = await service.get_menus(id)
        return response(menus)

    except Exception as e:
        return exception(500, e)

@router.post('/menu')
async def create (body: CreateMenu):
    try:
        menu = await service.create_menu(body)
        return response(menu)

    except UniqueViolationError:
        return exception(400)

    except Exception as e:
        return exception(500, e)

@router.patch('/menu/{id}')
async def update (body: UpdateMenu, id: str):
    try:
        menu = await service.update_menu(body, id)
        return response(menu)

    except UniqueViolationError:
        return exception(400)

    except Exception as e:
        return exception(500, e)

@router.delete('/menu/{id}')
async def delete (id: str):
    try:
        menu = await service.delete_menu(id)
        return response(menu)

    except AttributeError as e:
        return exception(404)

    except Exception as e:
        return exception(500, e)