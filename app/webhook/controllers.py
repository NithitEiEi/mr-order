from fastapi import APIRouter
import webhook.services as service
from handle.response import response
from webhook.models import WebhookBody
from handle.exception import exception

router = APIRouter()

@router.post('/webhook')
async def webhook (body: WebhookBody):
    try:
        result = await service.webhook(body)
        print(result)
        return response()
    
    except AttributeError as e:
        return exception(400)

    except Exception as e:
        print(e)
        return exception(500, e)