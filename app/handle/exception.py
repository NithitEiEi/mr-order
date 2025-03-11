from fastapi.responses import JSONResponse

def exception (code: int, detail = None):
    if code == 400:
        return JSONResponse(status_code= code, content= {
            "code": code,
            "message": "Bad Request"
        })

    if code == 401:
        return JSONResponse(status_code= code, content= {
            "code": code,
            "message": "Unauthorized"
        })

    if code == 404:
        return JSONResponse(status_code= code, content= {
            "code": code,
            "message": "Not Found"
        })

    if code == 500:
        return JSONResponse(status_code= code, content= {
            "code": code,
            "message": "Something Went Wrong",
            "detail": str(detail)
        })