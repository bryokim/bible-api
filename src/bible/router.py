from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated

from pythonbible.errors import InvalidVerseError

from src.bible.dependencies import (
    normalize_bible_version,
    validate_book,
    validate_chapter,
    validate_verse,
    validate_random_book,
    validate_random_chapter,
)
from src.bible.schemas import (
    AcceptedVersion,
    VerseResponse,
    AcceptedBookGroup,
)
from src.bible.service import get_parsed_verse, get_random_verse


bible_router = APIRouter(prefix="/bible", tags=["bible"])


@bible_router.get(
    "/verse",
    response_model=VerseResponse,
    status_code=status.HTTP_200_OK,
)
async def verse(
    book: str = Depends(validate_book),
    chapter: int = Depends(validate_chapter),
    verse: str = Depends(validate_verse),
    book_group: AcceptedBookGroup | None = AcceptedBookGroup.ANY,
    bible_version: AcceptedVersion | None = Depends(normalize_bible_version),
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


@bible_router.get("/random-verse")
async def random_verse(
    r_book: str | None = Depends(validate_random_book),
    r_chapter: str | None = Depends(validate_random_chapter),
    verse_range: Annotated[int, Query(gt=0, le=3)] = 1,
    book_group: AcceptedBookGroup = AcceptedBookGroup.ANY,
    bible_version: AcceptedVersion = Depends(normalize_bible_version),
):
    full_verse, verse_text = get_random_verse(
        r_book, r_chapter, verse_range, book_group, bible_version
    )

    return {
        "reference": full_verse,
        "verse_text": verse_text,
        "book_group": book_group.value if book_group else "",
        "bible_version": bible_version.value if bible_version else "",
    }
