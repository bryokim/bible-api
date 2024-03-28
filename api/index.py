from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.bible.router import bible_router

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    error = exc.errors()[0]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"detail": error["msg"], "loc": error["loc"]}
        ),
    )


@app.get("/api")
def root():
    return "Welcome to holy-text api"


app.include_router(bible_router, prefix='/api')
