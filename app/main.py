from fastapi import FastAPI
from shop.controllers import router as shop
from menu.controllers import router as menu
from slip.controllers import router as slip
from order.controllers import router as order
from stock.controllers import router as stock
from recipe.controllers import router as recipe
from webhook.controllers import router as webhook
from receipt.controllers import router as receipt
from ingredient.controllers import router as ingredient

app = FastAPI()

app.include_router(router=shop)
app.include_router(router=menu)
app.include_router(router=slip)
app.include_router(router=order)
app.include_router(router=stock)
app.include_router(router=recipe)
app.include_router(router=webhook)
app.include_router(router=receipt)
app.include_router(router=ingredient)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)