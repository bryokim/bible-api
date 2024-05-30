from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status

from pythonbible.errors import InvalidVerseError

from src.dependencies import (
    validate_book,
    validate_chapter,
    validate_verse,
    validate_reference,
    validate_random_chapter,
    validate_random_book,
)
from src.schemas import AcceptedBookGroup, AcceptedVersion, VerseResponse
from src.service import (
    get_parsed_verse,
)

router = APIRouter(prefix="/bible", tags=["bible v2"])


@router.get("/")
async def v2_root():
    return {"version": "2", "detail": "OK"}


@router.get("/today")
async def daily_verse(
    bible_version: AcceptedVersion = AcceptedVersion.NIV,
):
    return {"bible_version": bible_version}


@router.get("/random")
@router.get("/random/{r_book}")
@router.get("/random/{r_book}/{r_chapter}")
async def random_verse(
    r_book: str | None = Depends(validate_random_book),
    r_chapter: str | None = Depends(validate_random_chapter),
    verse_range: Annotated[int, Query(gt=0, le=3)] = 1,
    book_group: AcceptedBookGroup = AcceptedBookGroup.ANY,
    bible_version: AcceptedVersion = AcceptedVersion.NIV,
):
    return {
        "r_book": r_book,
        "r_chapter": r_chapter,
        "verse_range": verse_range,
        "book_group": book_group.value,
        "bible_version": bible_version,
    }


@router.get("/{reference}")
async def get_from_reference(
    reference: str = Depends(validate_reference),
    book_group: AcceptedBookGroup = AcceptedBookGroup.ANY,
    bible_version: AcceptedVersion = AcceptedVersion.NIV,
) -> VerseResponse:
    try:
        (_, _), verse_text = get_parsed_verse(reference, bible_version)
    except InvalidVerseError as e:
        raise HTTPException(status_code=404, detail=e.message)

    return {
        "reference": reference,
        "verse_text": verse_text,
        "book_group": book_group.value if book_group else "",
        "bible_version": bible_version,
    }


@router.get(
    "/{book}/{chapter}/{verse}",
    response_model=VerseResponse,
    status_code=status.HTTP_200_OK,
)
async def get_verse(
    book: str = Depends(validate_book),
    chapter: int = Depends(validate_chapter),
    verse: str = Depends(validate_verse),
    book_group: AcceptedBookGroup = AcceptedBookGroup.ANY,
    bible_version: AcceptedVersion = AcceptedVersion.NIV,
) -> VerseResponse:
    reference = f"{book.strip()} {chapter}:{verse.strip()}"

    try:
        (_, _), verse_text = get_parsed_verse(reference, bible_version)
    except InvalidVerseError as e:
        raise HTTPException(status_code=404, detail=e.message)

    return {
        "reference": reference,
        "verse_text": verse_text,
        "book_group": book_group.value if book_group else "",
        "bible_version": bible_version,
    }
