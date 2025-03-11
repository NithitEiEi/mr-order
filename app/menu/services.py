from prisma import Prisma
from handle.format import dump
from prisma.errors import UniqueViolationError
from menu.models import CreateMenu, UpdateMenu

prisma = Prisma()

async def get_menus (shop: str):
    try:
        await prisma.connect()
        menus = await prisma.menu.find_many(
            where={
                'shop': shop,
                'status': "ENABLE"
            },
            include={
                'recipe': {
                    'include': {
                        'Ingredient': True
                    }
                }
            }
        )
        menus = [dump(menu) for menu in menus]
        return menus


    finally:
        await prisma.disconnect()

async def create_menu (body: CreateMenu):
    try:
        await prisma.connect()
        menu = dump(body, exclude={"recipe"})
        recipes = dump(body, include={"recipe"}).get('recipe')
        exist = await prisma.menu.find_first(
                where={
                    'shop': menu['shop'],
                    'name': menu['name'],
                    'status': "ENABLE"
                }
            )
        if exist:
            exist = dump(exist)
            raise UniqueViolationError(menu)

        async with prisma.tx() as transaction:
            result = await transaction.menu.create(
                data=menu
            )

            if recipes:
                for recipe in recipes:
                    recipe['menu'] = result.id

                await transaction.recipe.create_many(
                    data=recipes
                )

        return dump(result)

    finally:
        await prisma.disconnect()

async def update_menu (body: UpdateMenu, id: str):
    try:
        await prisma.connect()
        menu = dump(body, exclude={"recipe"})
        recipes = dump(body, include={'recipe'}).get('recipe')
        async with prisma.tx() as transaction:
            result = await transaction.menu.update(
                where={
                    'id': id
                },
                data=menu
            )
            if recipes:
                await transaction.recipe.delete_many(
                    where={
                        'menu': result.id
                    }
                )
                for recipe in recipes:
                    recipe['menu'] = result.id

                await transaction.recipe.create_many(
                    data=recipes
                )
            if result is None:

                return dump(result)

        return dump(result)

    finally:
        await prisma.disconnect()

async def delete_menu (id: str):
    try:
        await prisma.connect()
        menu = await prisma.menu.update(
            where={
                'id': id,
            },
            data={
                'status': "DISABLE"
            }
        )
        return dump(menu)

    finally:
        await prisma.disconnect()