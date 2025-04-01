import os
import json
import httpx
from prisma import Prisma
from dotenv import load_dotenv
from handle.format import dump
from webhook.models import WebhookBody
from model.message import classify_order

prisma = Prisma()

load_dotenv()

timeout = httpx.Timeout(30.0)

async def webhook (body: WebhookBody):

    event = body.events[0]
    types = event.message.type
    sender = event.source['userId']
    group = event.source['groupId']
    reply = event.replyToken
    
    if types == 'image':
        image = event.message.id
        async with httpx.AsyncClient() as client:
            print("sending")
            response = await client.post(
                url="http://localhost:8000/slip",
                json={
                    "customer": sender,
                    "image": image
                },
                timeout=timeout
            )
            
        profile = await get_sender_profile(group, sender)
        name = profile['displayName']

        if response.status_code == 400:
            message = f"สลิปคุณ {name} ไม่ถูกต้องหรือใช้ซ้ำ"
            await callback(message, reply)
            return

        if response.status_code == 500:
            raise Exception("Something went wrong")

        data = response.text
        data = json.loads(data).get('data')

        remain = data['remain']
        if remain == 0:
            message = f"คุณ {name} โอนครบจำนวนครับ"

        if remain < 0:
            message = f"คุณ {name} โอนเงินเกินจำนวน ติดต่อผู้ขายเพื่อขอคืนเงิน"

        if remain > 0:
            message = f"คุณ {name} ยอดชำระขาดอีก {remain} บาท"

        await callback(message, reply)
        await prisma.disconnect()
        return

    if types == 'text':
        await prisma.connect()
        text = event.message.text
        mentions = event.message.mention.get('mentionees', {}) if event.message.mention else []
        
        if not mentions or (mentions and mentions[0].get('type') == "all"):
            await prisma.disconnect()
            return
        
        mentions = [mention.get('userId', []) for mention in mentions]
        menus = []

        sender_profile = await get_sender_profile(group, sender)
        
        for mention in mentions:
            shop = await prisma.shop.find_first(
                where={
                    'user': mention 
                },
                include={
                    'menu': {
                        'where': {
                            'status': "ENABLE"
                        }
                    }
                }
            )
            if not shop:
                raise AttributeError("Bad request")
            
            menus = shop.menu
            shop = shop.id if shop is not None else ""
            order = await prisma.order.find_first(
                where={
                    'shop': shop,
                    'customer': sender,
                    'process': "PENDING"
                }
            )
            old_order = dump(order, include={'payment', 'address', 'detail'}) if order else {}
            menus = [dump(menu, exclude={'shop'}) for menu in menus]
            generate = await classify_order(text, menus, old_order)

            await prisma.disconnect()
            
            if generate['intent'] == "make" and not order:
                generate['customer'] = sender
                generate['shop'] = shop
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        url="http://localhost:8000/order",
                        json=generate
                    )
                    message = f"รายการอาหารของคุณ {sender_profile['displayName']}\n"
                    orders = generate['detail']
                    for order in orders:
                        message += f"{order['name']} {order['amount']}\n"
                    message += f"ยอดทั้งหมด {generate['total']} บาท\n"
                    message += "สามารถเปลี่ยนรายการได้ครับ"
                    await callback(message, reply)

                return order

            if generate['intent'] == "update":
                async with httpx.AsyncClient() as client:
                    response = await client.patch(
                        url=f"http://localhost:8000/order/{order.id}",
                        json=generate
                    )

                    message = f"เปลี่ยนรายการของคุณ {sender_profile['displayName']} เป็น\n"
                    orders = generate['detail']
                    for order in orders:
                        message += f"{order['name']} {order['amount']}\n"
                    message += f"ยอดทั้งหมด {generate['total']} บาท\n"
                    message += "สามารถเปลี่ยนรายการได้ครับ"
                    await callback(message, reply)
                
                return orders
            
            if generate['intent'] == "cancel":
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        url=f"http://localhost:8000/order/{order.id}/cancel"
                    )

                    message = f" ยกเลิกรายการของคุณ {sender_profile['displayName']} เรียบร้อยแล้วครับ"
                    await callback(message, reply)
                
                return response.text

async def callback(message: str, reply: str):

    async with httpx.AsyncClient() as client:
        data = {
            'replyToken': reply,
            'messages': [
                {
                    "type": "text",
                    "text": message
                }    
            ],
        }

        callback_response = await client.post(
            url="https://api.line.me/v2/bot/message/reply",
            headers={
                "Authorization": f"Bearer {os.getenv('CHANNEL_ACCESS_TOKEN')}",
                "Content-Type": "application/json"
            },
            json=data,
            timeout=timeout
        )

        return callback_response.text



async def get_sender_profile(group: str, mention: str):
    url = f"https://api.line.me/v2/bot/group/{group}/member/{mention}"
    header = {
        "Authorization": f"Bearer {os.getenv('CHANNEL_ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url, headers=header)
    
    return response.json()