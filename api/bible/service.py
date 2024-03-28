import pythonbible as bible

from api.bible.schemas import AcceptedVersion, AcceptedBookGroup
from api.bible.utils import random_full_verse, get_book


def get_verse_text(verse: str, bible_version: bible.Version):
    reference = bible.get_references(verse)
    verse_ids = bible.convert_references_to_verse_ids(reference)
    text = bible.format_scripture_text(
        verse_ids,
        format_type="json",
        one_verse_per_paragraph=True,
        version=bible_version,
    )
    return text


def get_parsed_verse(
    verse: str,
    bible_version: (
        bible.Version | AcceptedVersion
    ) = bible.Version.NEW_INTERNATIONAL,
) -> tuple[tuple[str, str], list[str]]:
    """Parses a verse into the book, chapter and requested verses' text.

    Args:
        verse (str): The verse(s) to get. Example `Genesis 1:1-4`
        bible_version (bible.Version, optional): The version of the bible to
            use. Defaults to `New International Version (NIV)`.

    Returns:
        tuple[tuple[str, str], list[str]]: A tuple of a tuple of book and
        chapter and a list of the text of all verses provided.

    Example:
    ```
        book_and_chapter, verses = get_parsed_verse("Genesis 1:1-2")

        print(book_and_chapter) # ('Genesis', 'Chapter 1')
        for verse in verses:
            print(verse) # Prints verse 1 and 2 of Genesis chapter 1 depending
                         # on the version of the bible.
    ```
    """
    if isinstance(bible_version, AcceptedVersion):
        bible_version = bible.Version[bible_version.value]

    text = get_verse_text(verse, bible_version=bible_version)

    text_list = list(filter(lambda x: x != "", text.split("\n")))

    try:
        book_and_chapter, verses = (text_list[0], text_list[1]), text_list[2:]
    except IndexError:
        raise bible.errors.InvalidVerseError("Invalid verse entered")

    return book_and_chapter, verses


def get_random_verse(
    r_book: str | None = None,
    r_chapter: int | None = None,
    verse_range: int = 0,
    book_group: AcceptedBookGroup = AcceptedBookGroup.ANY,
    bible_version: (
        bible.Version | AcceptedVersion
    ) = bible.Version.NEW_INTERNATIONAL,
) -> tuple[str, str]:

    _book = get_book(r_book) if r_book else None
    _book_group = book_group.pythonbible_book_group()

    full_verse = random_full_verse(_book, r_chapter, verse_range, _book_group)

    (_, _), verse_text = get_parsed_verse(full_verse, bible_version)

    return full_verse, verse_text
