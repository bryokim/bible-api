from fastapi import HTTPException

from pythonbible.bible import titles
from pythonbible.validator import is_valid_chapter, is_valid_verse

from src.schemas import AcceptedBookGroup, AcceptedVersion
from src.utils import get_book, parse_reference


def validate_book(
    book: str,
    book_group: AcceptedBookGroup = AcceptedBookGroup.ANY,
    bible_version: AcceptedVersion = AcceptedVersion.NIV,
) -> str:
    """Check to see if the given Book is a valid book of the Bible
    and can be found in the given book group and bible version.

    Args:
        book (str): Book of the bible being requested
        book_group (AcceptedBookGroup, optional): a group of the books of the
            bible. Defaults to AcceptedBookGroup.ANY.
        bible_version (AcceptedVersion, optional): Bible version to use.
            Defaults to NIV.

    Raises:
        HTTPException: Raised if the book does not match any of the
            given books in Book.
        HTTPException: Raised if the book is not in the given book group.
        HTTPException: Raised if the book is not found in the given Bible
            version.
        HTTPException: Raised if the book is not found in the given book group.

    Returns:
        str: title of the matched book.
    """

    _book = get_book(book)
    _pythonbible_version = bible_version.pythonbible_version()

    if _book:
        if not (
            book_group is book_group.ANY
            or _book in book_group.pythonbible_book_group().books #pyright:ignore[reportOptionalMemberAccess]
        ):
            raise HTTPException(
                status_code=400,
                detail="{} not in {} group".format(
                    _book.title, book_group.value
                ),
            )
        elif _book not in titles.SHORT_TITLES[_pythonbible_version].keys():
            raise HTTPException(
                status_code=400,
                detail="{} not in {}".format(
                    _book.title, _pythonbible_version.title
                ),
            )
        else:
            return _book.title

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


def validate_reference(
    reference: str | None = None,
    book: str | None = None,
    chapter: int | None = None,
    verse: str | None = None,
):
    """Check if the given reference is valid.

    Args:
        reference (str | None, optional): Verse with book, chapter and verse.
            Defaults to None.
        book (str | None, optional): Book of the bible. Defaults to None.
        chapter (int | None, optional): Chapter of the book. Defaults to None.
        verse (str | None, optional): Verse of the chapter. Defaults to None.

    Raises:
        HTTPException: If the book is not given and cannot be gotten from reference.
        HTTPException: If the chapter is not given and cannot be gotten from reference.
        HTTPException: If the verse is not given and cannot be gotten from reference.

    Returns:
        str: A string of the reference that is validated.
    """

    if reference is not None:
        book, chapter, verse = parse_reference(reference)

    if book is None:
        raise HTTPException(
            status_code=400,
            detail="Must provide `book` if `reference` is not given",
        )

    if chapter is None:
        raise HTTPException(
            status_code=400,
            detail="Must provide `chapter` of `{}` to get.".format(book),
        )

    if verse is None:
        raise HTTPException(
            status_code=400,
            detail="Must provide `verse` of `{} {}` to get.`".format(
                book, chapter
            ),
        )

    _book = validate_book(book)
    _chapter = validate_chapter(book, chapter)
    _verse = validate_verse(verse, book, chapter)

    return f"{_book.strip()} {_chapter}:{_verse.strip()}"


def validate_random_book(
    r_book: str | None = None,
    book_group: AcceptedBookGroup = AcceptedBookGroup.ANY,
    bible_version: AcceptedVersion = AcceptedVersion.NIV,
) -> str | None:
    """Check to see if the given book is a valid book and is in the given group
    and can be found in given bible version.

    Args:
        r_book (str | None, optional): a book of the bible. Defaults to None.
        book_group (AcceptedBookGroup, optional): a group of the books of the
            bible. Defaults to AcceptedBookGroup.ANY.
        bible_version (AcceptedVersion, optional): Bible version to use.
            Defaults to NIV.

    Returns:
        str | None: Validated book of the bible. None if r_book is None
    """

    if not r_book:
        return None

    return validate_book(r_book, book_group, bible_version)


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
    elif not r_book:
        raise HTTPException(
            status_code=400, detail="cannot provide chapter without book"
        )

    return validate_chapter(r_book, r_chapter)
