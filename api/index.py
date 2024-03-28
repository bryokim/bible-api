from typing import Union

from fastapi import Depends, FastAPI, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from pythonbible.errors import InvalidVerseError

from api._bible.router import bible_router

from api._bible.dependencies import (
    normalize_bible_version,
    validate_book,
    validate_chapter,
    validate_verse,
)
from api._bible.schemas import (
    AcceptedVersion,
    VerseResponse,
    AcceptedBookGroup,
)
from api._bible.service import get_parsed_verse

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


@app.get("/api/verse")
async def verse(
    book: str = Depends(validate_book),
    chapter: int = Depends(validate_chapter),
    verse: str = Depends(validate_verse),
    book_group: Union[AcceptedBookGroup, None] = AcceptedBookGroup.ANY,
    bible_version: Union[AcceptedVersion, None] = Depends(
        normalize_bible_version
    ),
) -> VerseResponse:
    full_verse = f"{book.strip()} {chapter}:{verse.strip()}"

    try:
        (_book, _chapter), verse_text = get_parsed_verse(
            full_verse, bible_version
        )
    except InvalidVerseError as e:
        raise HTTPException(status_code=404, detail=e.message)

    return {
        "reference": "{} {}:{}".format(_book, _chapter, verse),
        "verse_text": verse_text,
        "version": bible_version,
    }


app.include_router(bible_router, prefix="/api")
