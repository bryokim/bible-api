import re

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated

from pythonbible.errors import InvalidVerseError

from src.dependencies import (
    validate_reference,
    validate_random_book,
    validate_random_chapter,
)
from src.schemas import (
    DailyVerseResponse,
    AcceptedVersion,
    VerseResponse,
    AcceptedBookGroup,
)
from src.service import (
    get_parsed_verse,
    get_random_verse,
    get_daily_verse,
)


bible_router = APIRouter(prefix="/bible", tags=["bible"])


@bible_router.get(
    "/verse",
    response_model=VerseResponse,
    status_code=status.HTTP_200_OK,
)
async def verse(
    reference: str = Depends(validate_reference),
    book_group: AcceptedBookGroup = AcceptedBookGroup.ANY,
    bible_version: AcceptedVersion = AcceptedVersion.NIV,
) -> VerseResponse:
    try:
        (_book, _chapter), verse_text = get_parsed_verse(
            reference, bible_version
        )
    except InvalidVerseError as e:
        raise HTTPException(status_code=404, detail=e.message)

    # Get verse from the reference
    mo = re.search(r":.+", reference)
    _verse = mo.group() if mo else ""

    return {
        "reference": "{} {}{}".format(_book.strip(), _chapter.strip(), _verse),
        "verse_text": verse_text,
        "book_group": book_group.value if book_group else "",
        "bible_version": bible_version,
    }


@bible_router.get("/random-verse")
async def random_verse(
    r_book: str | None = Depends(validate_random_book),
    r_chapter: str | None = Depends(validate_random_chapter),
    verse_range: Annotated[int, Query(gt=0, le=3)] = 1,
    book_group: AcceptedBookGroup = AcceptedBookGroup.ANY,
    bible_version: AcceptedVersion = AcceptedVersion.NIV,
) -> VerseResponse:
    reference, verse_text = get_random_verse(
        r_book, r_chapter, verse_range, book_group, bible_version
    )

    return {
        "reference": reference,
        "verse_text": verse_text,
        "book_group": book_group.value if book_group else "",
        "bible_version": bible_version.value if bible_version else "",
    }


@bible_router.get("/daily-verse")
async def daily_verse(
    bible_version: AcceptedVersion = AcceptedVersion.NIV,
) -> DailyVerseResponse:
    verse = get_daily_verse(bible_version)
    return verse
