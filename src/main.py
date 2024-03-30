import os

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.bible.router import bible_router

app = FastAPI()

LOCALHOST = os.getenv("BIBLE_UI_HOST", "")

origins = ["bible-ui-two.vercel.app"]

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


@app.get("/")
def root():
    return "Welcome to holy-text"


app.include_router(bible_router)
