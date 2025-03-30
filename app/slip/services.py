import os
import io
import re
import httpx
import json
from PIL import Image
from prisma import Prisma
from dotenv import load_dotenv
from handle.format import dump
from slip.models import CreateSlip
from slip.models import WebhookSlip
from model.gemini import classify_img
from model.prompt import slip_prompt
from prisma.errors import RecordNotFoundError

prisma = Prisma()

load_dotenv()

async def create_slip(body: WebhookSlip):
    try:
        await prisma.connect()
        url = f"https://api-data.line.me/v2/bot/message/{body.image}/content"
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=url,
                headers={
                    "Authorization": f"Bearer {os.getenv('CHANNEL_ACCESS_TOKEN')}"
                }
            )

            image = Image.open(io.BytesIO(response.content))

            generate = await classify_img(image, slip_prompt)
            clean = re.sub('json', '', generate).strip("`")
            result = json.loads(clean)

        if result['type'] == "slip":
            print("in if")
            shop = await prisma.shop.find_first(
                where={
                    'account': result['receiver']
                }
            )

            order = await prisma.order.find_first(
                where={
                    'customer': body.customer,
                    'shop': shop.id,
                    'process': "PENDING",
                    'payment': "TRANSFER"
                }
            )
            if not shop:
                raise RecordNotFoundError
            
            if not order:
                raise AttributeError
            
            data = result
            data['order'] = order.id
            del data['type']
            price = order.total
            async with prisma.tx() as transaction:
                data['status'] = "VALID" if data['amount'] == price else "INVALID"

                slip = await transaction.slip.create(
                    data=data
                )
                remain = order.total - slip.amount
                
                order = await transaction.order.update(
                    where={
                        'id': slip.order
                    },
                    data={
                        "remain": remain
                    }
                )
            print("order", dump(order))
            return dump(order)
            
    finally:
        await prisma.disconnect()