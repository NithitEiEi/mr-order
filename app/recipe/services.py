from prisma import Prisma
from handle.format import dump

prisma = Prisma()

async def delete_recipe (menu: str, ingredient: str):
    try:
        await prisma.connect()
        recipe = await prisma.recipe.delete(
            where={
                'menu_ingredient': {
                    'menu': menu,
                    'ingredient': ingredient
                }
            }
        )
        return dump(recipe)

    finally:
        await prisma.disconnect()