import json
from prisma import Prisma
from handle.format import dump
import order.calculate as calculate
from order.models import CreateOrder, UpdateOrder

prisma = Prisma()

async def get_order (shop: str):
    try:
        await prisma.connect()
        orders = await prisma.order.find_many(
            where={
                'shop': shop,
                'process': {'in': ['PENDING', 'DONE']}
            },
            include={
                'slip': True
            }
        )
        orders = [dump(order, exclude={'shop'}) for order in orders]

        return orders

    finally:
        await prisma.disconnect()


async def get_detail (id: str):
    try:
        await prisma.connect()
        order = await prisma.order.find_first(
            where={
                'id': id
            },
            include={
                'detail': True
            }
        )
        order = dump(order, exclude={'shop'})
        details = order['detail']
        
        for detail in details:
            menu = await prisma.menu.find_first(
                where={
                    'id': detail['menu']
                },
                include={
                    'recipe': True
                }
            )
            detail['name'] = menu.name
            detail['price'] = menu.price
            
        order['detail'] = details
        return order

    finally:
        await prisma.disconnect()

async def get_oreder_usage (shop: str):
    try:
        await prisma.connect()
        orders = await prisma.order.find_many(
            where={
                'shop': shop,
                'process': "PENDING"
            },
            include={
                'detail': {
                    'include': {
                        'Menu': {
                            'include': {
                                'recipe': True
                            }
                        }
                    }
                }
            }
        )
        orders = [dump(order) for order in orders]
        usages = calculate.usage(orders)
        for usage in usages:
            ingredient = await prisma.ingredient.find_first(
                where={
                    'id': usage['ingredient']
                }
            )

            stocks = await prisma.stock.find_many(
                where={'ingredient': ingredient.id},
            )

            sum_stock = float(sum(stock.remain for stock in stocks))
            usage['name'] = ingredient.name
            usage['unit'] = ingredient.unit
            usage['remain'] = sum_stock

        return usages

    finally:
        await prisma.disconnect()

async def create_order (body: CreateOrder):
    try:
        await prisma.connect()
        data = dump(body, exclude={'detail'})
        data['remain'] = body.total
        details = body.detail
        details = [dump(detail) for detail in details]
        async with prisma.tx() as transaction:
            result = await transaction.order.create(
                data=data,
                include={
                    'detail': True
                }
            )
            for detail in details:
                detail['order'] = result.id

            await transaction.orderdetail.create_many(
                data=details
            )
        return dump(result)

    finally:
        await prisma.disconnect()

async def cancel_order (id: str):
    try:
        await prisma.connect()
        result = await prisma.order.update(
            where={
                'id': id
            },
            data={
                'process': "CANCEL"
            }
        )
        return dump(result)

    finally:
        await prisma.disconnect()

async def complete_order(id: str):
    try:
        await prisma.connect()
        order = await prisma.order.update(
            where={
                'id': id
            },
            data={
                'process': "COMPLETE"
            }
        )
        return dump(order)

    finally:
        await prisma.disconnect()

async def done_order(id: str):
    try:
        await prisma.connect()
        order = await prisma.order.find_first(
            where={'id': id},
            include={
                'detail': {
                    'include': {
                        "Menu": {
                            'include': {
                                'recipe': True
                            }
                        }
                    }
                }
            }
        )

        if order.process == "DONE":
            raise ValueError

        order = dump(order)
        usages = calculate.usage([order])
        
        async with prisma.tx() as transaction:
            result = await transaction.order.update(
                where={'id': id},
                data={'process': "DONE"}
            )
            
            for usage in usages:
                amount = usage['amount']
                
                all_stocks = await transaction.stock.group_by(
                    by=['status', 'ingredient'],
                    sum={'remain': True},
                    where={
                        'status': 'AVAILABLE',
                        'ingredient': usage['ingredient']
                    }
                )
                
                all_stocks = all_stocks[0]['_sum']['remain'] if all_stocks else 0
                if all_stocks < amount:
                    raise ValueError("Ingredient required more than in stocks")
                
                stocks = await transaction.stock.find_many(
                    where={
                        'ingredient': usage['ingredient'],
                        'status': "AVAILABLE"
                    },
                    order={'add_date': 'asc'}
                )
                
                for stock in stocks:
                    if amount <= 0:
                        break
                    
                    stock_remain = stock.remain
                    if stock_remain > amount:
                        await transaction.stock.update(
                            where={'id': stock.id},
                            data={'remain': stock_remain - amount}
                        )
                        amount = 0
                    else:
                        await transaction.stock.update(
                            where={'id': stock.id},
                            data={'remain': 0, 'status': 'EXPIRE'}
                        )
                        amount -= stock_remain
            
        return dump(result)
    
    finally:
        await prisma.disconnect()

async def update_order (body: UpdateOrder, id: str):
    try:
        await prisma.connect()
        data = dump(body, exclude={'detail'})
        details = dump(body, include={'detail'}).get('detail')    

        async with prisma.tx() as transaction:
            result = await transaction.order.update(
                where={
                    'id': id
                },
                data=data,

            )

            if details:
                await transaction.orderdetail.delete_many(
                    where={
                        'order': result.id
                    }
                )
                for detail in details:
                    detail['order'] = result.id

                await transaction.orderdetail.create_many(
                    data=details
                )

        return dump(result)

    finally:
        await prisma.disconnect()