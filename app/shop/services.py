from prisma import Prisma
from handle.format import dump
from shop.models import CreateShop, UpdateShop

prisma = Prisma()

async def get_shop (line: str):
    try:
        await prisma.connect()
        shop = await prisma.shop.find_unique(
            where={
                'user': line
            }
        )
        return dump(shop)

    finally:
        await prisma.disconnect()

async def create_shop (body: CreateShop):
    try:
        await prisma.connect()
        data = dump(body)
        shop = await prisma.shop.create(
            data=data
        )
        return dump(shop)

    finally:
        await prisma.disconnect()

async def update_shop (body: UpdateShop, id: str):
    try:
        await prisma.connect()
        data = dump(body)
        shop = await prisma.shop.update(
            where={
                'id': id
            },
            data=data
        )
        return dump(shop)

    finally:
        await prisma.disconnect()

async def delete_shop (id: str):
    try:
        await prisma.connect()
        shop = await prisma.shop.delete(
            where={
                'id': id
            }
        )
        return dump(shop)

    finally:
        await prisma.disconnect()