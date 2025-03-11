from prisma import Prisma
from handle.format import dump
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from stock.models import CreateStock, UpdateStock

prisma = Prisma()

def calculate_expire(amount, unit):
    if unit == "DAY":
        return relativedelta(days=amount)
    elif unit == "WEEK":
        return relativedelta(weeks=amount)
    elif unit == "MONTH":
        return relativedelta(months=amount)
    elif unit == "YEAR":
        return relativedelta(years=amount)
    return relativedelta(days=0)

async def create_stocks (bodies: list[CreateStock]):
    try:
        await prisma.connect()
        now = datetime.now(timezone.utc)
        data = []
        for body in bodies:
            ingredient = await prisma.ingredient.find_first(
                where={
                    'id': body.ingredient
                }
            )
            stock = dump(body)
            stock['add_date'] = datetime.now(timezone.utc)
            stock['expire'] = now + calculate_expire(ingredient.ages, ingredient.ages_unit)
            data.append(stock)

        stocks = await prisma.stock.create_many(
            data=data
        )
        return stocks

    finally:
        await prisma.disconnect()

async def update_stock (body: UpdateStock, id: str):
    try:
        await prisma.connect()
        data = dump(body)
        stock = await prisma.stock.update(
            where={
                'id': id
            },
            data=data
        )
        return dump(stock)

    finally:
        await prisma.disconnect()

async def delete_stock (id: str):
    try:
        await prisma.connect()
        stock = await prisma.stock.delete(
            where={
                'id': id
            }
        )
        return dump(stock)

    finally:
        await prisma.disconnect()