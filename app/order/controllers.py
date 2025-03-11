from fastapi import APIRouter
import order.services as service
from handle.response import response
from handle.exception import exception
from order.models import CreateOrder, UpdateOrder

router = APIRouter()

@router.get('/shop/{shop}/order')
async def get (shop: str):
    try:
        orders = await service.get_order(shop)
        return response(orders)
    
    except Exception as e:
        return exception(500, e)
    
@router.get('/shop/{shop}/usage')
async def get_usage (shop: str):
    try:
        usage = await service.get_oreder_usage(shop)
        return response(usage)

    except Exception as e:
        return exception(500, e)
    
@router.get('/order/{id}')
async def get_detail (id: str):
    try:
        detail = await service.get_detail(id)
        return response(detail)
    
    except Exception as e:
        return exception(500, e)
    
@router.post('/order')
async def create (body: CreateOrder):
    try:
        order = await service.create_order(body)
        return response(order)

    except Exception:
        return exception(400)

    except Exception as e:
        return exception(500, e)
    
@router.post('/order/{id}/cancel')
async def cancel (id: str):
    try:
        order = await service.cancel_order(id)
        return response(order)
    
    except Exception as e:
        return exception(500, e)
    
@router.post('/order/{id}/done')
async def done (id: str):
    try:
        order = await service.done_order(id)
        return response(order)
    
    except ValueError:
        return exception(400)

    except Exception as e:
        return exception(500, e)
    
@router.patch('/order/{id}')
async def update (body: UpdateOrder, id: str):
    try:
        order = await service.update_order(body, id)
        return response(order)

    except Exception as e:
        return exception(500, e)