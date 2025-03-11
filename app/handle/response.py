from fastapi.responses import JSONResponse

def response (data: dict = None):
    return JSONResponse(status_code= 200, content= {
        "code": 200,
        "message": "Success",
        "data": data
    })