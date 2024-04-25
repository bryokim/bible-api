import os

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

DESCRIPTION = """
Get Bible verses.
"""

app = FastAPI(
    title="Bible API",
    description=DESCRIPTION,
    version='0.1.1'
)

LOCALHOST = os.getenv("BIBLE_UI_HOST", "")

origins = ["https://bible-ui-two.vercel.app"]

if LOCALHOST:
    origins.append(LOCALHOST)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
