from typing import Union

from fastapi import Depends, APIRouter, HTTPException

from pythonbible.errors import InvalidVerseError

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


router = APIRouter()

@router.get("/api/verse")
async def handler(
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
