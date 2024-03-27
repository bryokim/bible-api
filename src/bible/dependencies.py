from fastapi import HTTPException

from pythonbible.validator import is_valid_chapter, is_valid_verse

from src.bible.constants import SHORT_VERSION_NAMES
from src.bible.schemas import AcceptedBookGroup, AcceptedVersion
from src.bible.utils import get_book


def normalize_bible_version(
    bible_version: AcceptedVersion = AcceptedVersion.NIV,
) -> AcceptedVersion:
    """Converts short version names into long names that can be easily
    passed to pythonbible module.

    Args:
        bible_version (AcceptedVersions): Bible version that client has requested.

    Returns:
        AcceptedVersions: Normalized bible version.
    """
    if bible_version.value in SHORT_VERSION_NAMES:
        return AcceptedVersion[bible_version.value]

    return bible_version


def validate_book(
    book: str,
    book_group: AcceptedBookGroup = AcceptedBookGroup.ANY,
) -> str:
    """Check to see if the given Book is a valid book of the Bible.

    Args:
        book (str): Book of the bible being requested

    Raises:
        HTTPException: Raised if the book does not match any of the
            given books in Book.
        HTTPException: Raised if the book is not in the given book group.

    Returns:
        str: title of the matched book.
    """

    _book = get_book(book)

    if _book:
        if (
            book_group is book_group.ANY
            or _book in book_group.pythonbible_book_group().books
        ):
            return _book.title
        else:
            raise HTTPException(
                status_code=400,
                detail="{} not in {} group".format(
                    _book.title, book_group.value
                ),
            )

    raise HTTPException(status_code=400, detail="{} not found".format(book))


def validate_chapter(book: str, chapter: int) -> int:
    """Check to see if the given chapter is a valid chapter of a given book.

    Args:
        book (str): a book of the bible
        chapter (int): Chapter to check.

    Raises:
        HTTPException: Raised if the chapter is invalid.
        HTTPException: Raised if the book is invalid.

    Returns:
        int: Validated chapter
    """

    _book = get_book(book)

    if not _book:
        raise HTTPException(
            status_code=400, detail="{} not found".format(book)
        )

    if is_valid_chapter(_book, chapter):
        return chapter

    raise HTTPException(
        status_code=400,
        detail="Chapter {} not found in {}".format(chapter, book),
    )


def validate_verse(verse: str, book: str, chapter: int) -> str:
    """Check to see if the given verse is a valid verse of the
    chapter of a given book.

    Args:
        verse (str): verse to check.
        book (str): a book of the bible
        chapter (int): a chapter of the book.

    Raises:
        HTTPException: Raised if the verse cannot be cast into an integer.
        HTTPException: Raised if the verse is invalid.

    Returns:
        str: Validated verse
    """

    _book = get_book(book)

    if not _book:
        raise HTTPException(
            status_code=400, detail="{} not found".format(book)
        )

    try:
        from_verse, to_verse = (
            verse.split("-", 1) if "-" in verse else [verse, verse]
        )

        from_verse = int(from_verse)
        to_verse = int(to_verse)

        if from_verse > to_verse:
            raise HTTPException(
                status_code=400,
                detail="start verse ({}) cannot be greater than end verse ({})".format(
                    from_verse, to_verse
                ),
            )

        if from_verse <= 0:
            raise HTTPException(
                status_code=400,
                detail="verse ({}) cannot be less than 1".format(from_verse),
            )

        if is_valid_verse(_book, chapter, to_verse):
            return (
                "{}-{}".format(from_verse, to_verse)
                if from_verse != to_verse
                else "{}".format(from_verse)
            )

    except ValueError:
        raise HTTPException(
            status_code=400, detail="verse cannot be converted to int"
        )

    raise HTTPException(
        status_code=400,
        detail="verse {} not found in {} {}".format(
            verse, _book.title, chapter
        ),
    )


def validate_random_book(
    r_book: str | None = None,
    book_group: AcceptedBookGroup = AcceptedBookGroup.ANY,
) -> str | None:
    """Check to see if the given book is a valid book and is in the given group

    Args:
        r_book (str | None, optional): a book of the bible. Defaults to None.
        book_group (AcceptedBookGroup, optional): a group of the books of the
            bible. Defaults to AcceptedBookGroup.ANY.

    Returns:
        str | None: Validated book of the bible. None if r_book is None
    """

    if not r_book:
        return None

    return validate_book(r_book, book_group)


def validate_random_chapter(
    r_book: str | None = None, r_chapter: int | None = None
) -> int | None:
    """Check to see if the given chapter is a valid chapter of a given book.

    Args:
        r_book (str | None): a book of the bible. Defaults to None.
        r_chapter (int | None): Chapter to check. Defaults to None.

    Raises:
        HTTPException: Raised if the r_chapter is given and r_book isn't given.

    Returns:
        int | None: Validated chapter. None if r_chapter is None
    """

    if not r_chapter:
        return None

    if r_chapter and not r_book:
        raise HTTPException(
            status_code=400, detail="cannot provide chapter without book"
        )

    return validate_chapter(r_book, r_chapter)
