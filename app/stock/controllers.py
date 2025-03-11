from fastapi import APIRouter
import stock.services as service
from handle.response import response
from handle.exception import exception
from stock.models import CreateStock, UpdateStock

router = APIRouter()

@router.post('/stock')
async def create (body: list[CreateStock]):
    try:
        stocks = await service.create_stocks(body)
        return response(stocks)

    except Exception as e:
        return exception(500, e)

@router.patch('/ingredient/{id}/stock')
async def update (body: UpdateStock, id: str):
    try:
        stock = await service.update_stock(body, id)
        return response(stock)

    except Exception as e:
        return exception(500, e)

@router.delete('/ingredient/{id}/stock')
async def delete (id: str):
    try:
        stock = await service.delete_stock(id)
        return response(stock)

    except Exception as e:
        return exception(500, e)