import os
import io
import re
import httpx
import json
from PIL import Image
from prisma import Prisma
from dotenv import load_dotenv
from handle.format import dump
from slip.models import WebhookSlip
from model.prompt import slip_prompt
from model.gemini import classify_img

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

        if result['type'] != "slip":
            return
        
        shop = await prisma.shop.find_first(
            where={
                'OR': [
                    {'account': result['receiver']},
                    {'account_eng': result['receiver']}
                ]
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

        existed = await prisma.slip.find_first(
            where={
                'ref': result['ref']
            }
        )

        if not order or not shop or existed:
            raise AttributeError()
        
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
        
        return dump(order)
            
    finally:
        await prisma.disconnect()