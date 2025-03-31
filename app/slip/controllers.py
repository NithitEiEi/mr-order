from fastapi import APIRouter
import slip.services as service
from slip.models import WebhookSlip
from handle.response import response
from handle.exception import exception
from prisma.errors import UniqueViolationError

router = APIRouter()

@router.post('/slip')
async def create (body: WebhookSlip):
    try:
        slip = await service.create_slip(body)
        return response(slip)
    
    except AttributeError as e:
        print(e)
        return exception(400)

    except Exception as e:
        return exception(500, e)