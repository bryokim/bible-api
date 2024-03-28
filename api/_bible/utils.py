import random
import re

from functools import lru_cache
from typing import Union

from pythonbible.books import Book
from pythonbible.book_groups import BookGroup
from pythonbible.validator import is_valid_chapter
from pythonbible.verses import MAX_VERSE_NUMBER_BY_BOOK_AND_CHAPTER

from api._bible.exceptions import InvalidArgumentsError


@lru_cache
def get_book(book: str) -> Union[Book, None]:
    """Gets a Book with a regex matching book.

    Args:
        book (str): name of the book to get.

    Returns:
        Book | None: A value from the Book enum or None.
    """
    for _book in Book:
        if re.search(
            _book.regular_expression,
            book,
            re.IGNORECASE,
        ):
            return _book


def random_book(book_group: Union[BookGroup, None] = None) -> Book:
    """Returns random book from the Bible. If book_group is given, the
    book is chosen from that group.

    Args:
        book_group (BookGroup | None, optional): a book group to get from.
            Defaults to None.

    Returns:
        Book: a random book of the Bible
    """
    allowed_books = []

    if book_group:
        # Books in the selected group only
        allowed_books = list(book_group.books)
    else:
        # All books
        allowed_books = list(Book)

    return random.choice(allowed_books)


def random_chapter_from_book(book: Book) -> int:
    """Gets a random chapter from a book

    Args:
        book (Book): book to get a chapter from

    Returns:
        int: random chapter from book
    """
    number_chapters = len(MAX_VERSE_NUMBER_BY_BOOK_AND_CHAPTER.get(book))

    return random.choice(range(1, number_chapters + 1))


def random_full_verse(
    book: Union[Book, None] = None,
    chapter: Union[int, None] = None,
    verse_range: int = 1,
    book_group: Union[BookGroup, None] = None,
) -> str:
    """Gets a random verse.

    Args:
        book (Book | None, optional): if given, verse is from this book.
            Defaults to None.
        chapter (int | None, optional): if given, verse is from this chapter.
            Defaults to None.
        verse_range (int, optional): number of verses to return. Defaults to 1.
        book_group (BookGroup | None, optional): if given, the book will be
            from this group. Defaults to None.

    Raises:
        InvalidArgumentsError: Raised if the chapter is given and book
            is not given.
        InvalidArgumentsError: Raised if chapter is not found in given book

    Returns:
        str: full verse

    Example:
    ```Python
    full_verse = random_full_verse(Book.Genesis, 1, 3)
    print(full_verse)   # Genesis 1:6-8

    full_verse = random_full_verse(verse_range=1, book_group=BookGroup.NEW_TESTAMENT_GOSPELS)
    print(full_verse)   # Mark 19:4-5
    ```
    """

    if not book and chapter:
        raise InvalidArgumentsError("Cannot provide chapter without book")

    if not book:
        _book = random_book(book_group=book_group)
        _chapter = random_chapter_from_book(_book)
    elif book and not chapter:
        _book = book
        _chapter = random_chapter_from_book(_book)
    else:
        _book = book

        if not is_valid_chapter(_book, chapter):
            raise InvalidArgumentsError(
                "chapter {} not in {}".format(chapter, _book.title)
            )

        _chapter = chapter

    number_verses = MAX_VERSE_NUMBER_BY_BOOK_AND_CHAPTER.get(_book)[
        _chapter - 1
    ]

    from_verse = random.choice(range(1, number_verses + 1 - verse_range))

    return (
        "{} {}:{}-{}".format(
            _book.title, _chapter, from_verse, from_verse + verse_range - 1
        )
        if verse_range > 1
        else "{} {}:{}".format(_book.title, _chapter, from_verse)
    )
