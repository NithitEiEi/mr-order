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
        print("before go", body)
        slip = await service.create_slip(body)
        print("slip", slip)
        return response(slip)
    
    except AttributeError:
        return exception(400)
    
    except AttributeError:
        return exception(404)

    except UniqueViolationError:
        return exception(400)

    except Exception as e:
        print(type(e), e)
        return exception(500, e)