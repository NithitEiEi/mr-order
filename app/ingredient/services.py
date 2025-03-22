from prisma import Prisma
from handle.format import dump
from ingredient.models import CreateIngredient, UpdateIngredient
from prisma.errors import UniqueViolationError

prisma = Prisma()

async def get_ingredients (shop: str):
    try:
        await prisma.connect()
        ingredients = await prisma.ingredient.find_many(
            where={
                'shop': shop
            },
            include={
                'stock': {
                    'where': {
                        'status': 'AVAILABLE'
                    }
                }
            }
        )

        ingredients = [dump(ingredient) for ingredient in ingredients]
        return ingredients

    finally:
        await prisma.disconnect()

async def create_ingredient (body: CreateIngredient):
    try:
        await prisma.connect()
        data = dump(body)
        exist = await prisma.ingredient.find_first(
            where={
                'shop': data['shop'],
                'name': data['name']
            }
        )
        if exist:
            raise UniqueViolationError(data)

        ingredient = await prisma.ingredient.create(
            data=data
        )
        return dump(ingredient)

    finally:
        await prisma.disconnect()

async def update_ingredient (body: UpdateIngredient, id: str):
    try:
        await prisma.connect()
        data = dump(body)
        ingredient = await prisma.ingredient.update(
            where={
                'id': id
            },
            data=data
        )
        return dump(ingredient)

    finally:
        await prisma.disconnect()

async def delete_ingredient (id: str):
    try:
        await prisma.connect()
        ingredient = await prisma.ingredient.delete(
            where={
                'id': id
            }
        )
        return dump(ingredient)

    finally:
        await prisma.disconnect()