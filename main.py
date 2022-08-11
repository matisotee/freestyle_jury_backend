from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from api_gateway.infrastructure.controllers.exceptions import HTTPException
from api_gateway.infrastructure.controllers import register_user, create_competition
from api_gateway.infrastructure.dependency_injection.injector import apply_api_gateway_injections
from competition.infrastructure.dependency_injection.injector import apply_competition_injections

app = FastAPI()

app.include_router(register_user.router)
app.include_router(create_competition.router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):

    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({
            'description': exc.description, 'error_code': exc.error_code
        }),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            'detail': exc.errors(),
            'error_code': 'FIELDS_ERROR'
        }),
    )


apply_api_gateway_injections()
apply_competition_injections()
