import io
import os
import re
import json
from PIL import Image
from prisma import Prisma
from handle.format import dump
from fastapi import UploadFile
from model.gemini import classify_img
from datetime import datetime, timezone
from model.prompt import receipt_prompt
from receipt.models import CreateReceipt, UpdateReceipt

prisma = Prisma()

async def get_receipts (shop: str):
    try:
        await prisma.connect()
        receipts = await prisma.receipt.find_many(
            where={
                'shop': shop
            },
            include={
                'detail': True
            }
        )
        receipts = [dump(receipt, exclude={'detail', 'shop'}) for receipt in receipts]
        return receipts

    finally:
        await prisma.disconnect()

async def get_receipt_detail (receipt: str):
    try:
        await prisma.connect()
        receipt = await prisma.receipt.find_first(
            where={
                'id': receipt
            },
            include={
                'detail': True
            }
        )

        return dump(receipt, exclude={'shop'})

    finally:
        await prisma.disconnect()

async def create_receipt (file: UploadFile, shop: str):
    try:
        await prisma.connect()
        file_bytes = await file.read()
        image = Image.open(io.BytesIO(file_bytes))
        ingredients = await prisma.ingredient.find_many(
            where={
                'shop': shop
            }
        )
        ingredients = [
            dump(ingredient, include={'id', 'name'}) for ingredient in ingredients
        ]

        today = datetime.now(timezone.utc)
        prompt = f"{receipt_prompt} {ingredients} \ntoday: {today}"
        response = await classify_img(image, prompt)
        result = re.sub('json', '', response, flags=re.IGNORECASE)
        result = result.strip("`")
        result = json.loads(result)

        if result['type'] != "receipt" or not result['detail']:
            raise ValueError()

        total = 0
        for detail in result['detail']:
            total += detail['price']

        result['total'] = total
        result['shop'] = shop
        result = CreateReceipt(**result)
        
        receipt = dump(result, exclude={'detail'})
        return_detail = dump(result, include={'detail'})
        details = dump(result, include={'detail'}).get('detail')

        async with prisma.tx() as transaction:
            result = await transaction.receipt.create(
                data=receipt
            )
            for detail in details:
                detail['receipt'] = result.id

            await transaction.receiptitem.create_many(
                data=details
            )

            upload_path = os.path.join(os.getcwd(), "upload")
            os.makedirs(upload_path, exist_ok=True)
            path = os.path.join(upload_path, f"{result.image}.jpg")
            image.save(path)
        
        return return_detail.get('detail')

    finally:
        await prisma.disconnect()

async def delete_receipt (id: str):
    try:
        await prisma.connect()
        receipt = await prisma.receipt.delete(
            where={
                'id': id
            }
        )
        upload_path = os.path.join(os.getcwd(), "upload")
        path = os.path.join(upload_path, f"{receipt.image}.jpg")
        
        if os.path.exists(path):
            os.remove(path)

        return receipt

    finally:
        await prisma.disconnect()