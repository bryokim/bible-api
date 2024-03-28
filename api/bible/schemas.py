from __future__ import annotations

from enum import Enum
from pydantic import BaseModel

from pythonbible import BookGroup

from api.bible.constants import MAPPED_BOOK_GROUPS


class AcceptedVersion(Enum):
    NIV = "NEW_INTERNATIONAL"
    ASV = "AMERICAN_STANDARD"
    KJV = "KING_JAMES"

    NIV_short = "NIV"
    ASV_short = "ASV"
    kJV_short = "KJV"


class Testament(Enum):
    ANY = "ANY"
    NEW = "New Testament"
    OLD = "Old Testament"


class AcceptedBookGroup(Enum):
    # Default value for matching all
    ANY = "Any"

    # Testaments
    NEW = "New Testament"
    OLD = "Old Testament"

    # Smaller groups
    LAW = "Law"
    HISTORY = "History"
    POETRY = "Poetry"
    WISDOM = "Wisdom"
    PROPHECY = "Prophecy"
    MAJOR_PROPHETS = "Major Prophets"
    MINOR_PROPHETS = "Minor Prophets"
    GOSPELS = "Gospels"
    EPISTLES = "Epistles"
    PAUL_EPISTLES = "Paul Epistles"
    GENERAL_EPISTLES = "General Epistles"
    APOCALYPTIC = "Apocalyptic"

    def pythonbible_book_group(self: AcceptedBookGroup) -> BookGroup:
        return MAPPED_BOOK_GROUPS[self.value]


class VerseResponse(BaseModel):
    reference: str
    verse_text: list[str]
    version: AcceptedVersion
