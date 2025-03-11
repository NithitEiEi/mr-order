import receipt.services as service
from handle.response import response
from handle.exception import exception
from receipt.models import CreateReceipt
from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter()

@router.get('/shop/{id}/receipt')
async def get (id: str):
    try:
        receipts = await service.get_receipts(id)
        return response(receipts)

    except Exception as e:
        return exception(500, e)
    
@router.get('/receipt/{id}')
async def get_detail (id: str):
    try:
        receipt = await service.get_receipt_detail(id)
        return response(receipt)
    
    except Exception as e:
        return exception(500, e)

@router.post('/receipt')
async def create (file: UploadFile = File(...), shop: str = Form(...)):
    try:
        receipt = await service.create_receipt(file, shop)
        return response(receipt)

    except Exception as e:
        return exception(500, e)

@router.delete('/receipt/{id}')
async def delete (id: str):
    try:
        receipt = await service.delete_receipt(id)
        return response(receipt)

    except Exception as e:
        return exception(500, e)