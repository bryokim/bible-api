from __future__ import annotations

import re

from datetime import date
from enum import StrEnum
from pydantic import BaseModel, validator

from pythonbible import BookGroup, Version

from src.bible.constants import MAPPED_BOOK_GROUPS, SHORT_VERSION_NAMES


class AcceptedVersion(StrEnum):
    NIV = "NEW_INTERNATIONAL"
    ASV = "AMERICAN_STANDARD"
    KJV = "KING_JAMES"

    NIV_short = "NIV"
    ASV_short = "ASV"
    kJV_short = "KJV"

    def pythonbible_version(self: AcceptedVersion) -> Version:
        """
        Returns pythonbible.Version equivalent of the AcceptedVersion

        Returns:
            Version: equivalent pythonbible Version.
        """

        _value = self.value

        if _value in SHORT_VERSION_NAMES:
            _value = AcceptedVersion[_value].value

        return Version[_value]


class AcceptedBookGroup(StrEnum):
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
    book_group: AcceptedBookGroup
    bible_version: AcceptedVersion


class DailyVerse(BaseModel):
    reference: str
    verse_text: list[str]
    bible_version: str
    day: date


class DailyVerseResponse(BaseModel):
    reference: str
    verse_text: list[str]
    bible_version: str
    day: str

    @validator("day", always=True, pre=True)
    def validate_date(cls, v: date) -> str:
        _ctime_date = v.ctime()  # Convert to ctime format

        # Remove extra spacing
        _ctime_date = re.sub(r"\s+", " ", _ctime_date)

        # Remove time details since its always 00:00:00
        _ctime_date = re.sub(r"00:00:00\s", "", _ctime_date)

        return _ctime_date
