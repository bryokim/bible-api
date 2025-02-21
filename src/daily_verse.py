import json

from datetime import date
from pathlib import Path
from typing import Any

from pythonbible import Version

from src.constants import DAILY_VERSE_FILE
from src.schemas import DailyVerse
from src.utils import random_reference


class DailyVerseStorage:
    """Class for handling DailyVerse"""

    __file_path = Path(DAILY_VERSE_FILE)
    __objects: dict[str, DailyVerse] = {}
    __reference: str = ""

    @property
    def reference(self) -> str:
        return self.__reference

    def __todays_verse(
        self, bible_version: Version = Version.NEW_INTERNATIONAL
    ) -> None:
        """Get new random verse of the day.
        Sets self.__reference to the random verse generated.

        Args:
            bible_version (Version, optional): Bible version to use.
                Defaults to Version.NEW_INTERNATIONAL.
        """
        self.__reference = random_reference(bible_version=bible_version)

    def get(self, bible_version: Version) -> DailyVerse | None:
        """Get the daily verse in a certain bible version.
        If the current daily verse is expired, a new reference is
        generated and None is returned.

        Args:
            bible_version (Version): Bible version to get the verse for

        Returns:
            DailyVerse | None: daily verse if found using the given version
                and the verse is valid for the day else None.
        """
        try:
            verse = self.__objects[bible_version.value]

            # Check if verse is expired
            if self._is_expired(verse):
                # Generate new verse for the day
                self.__todays_verse()
                # Remove any saved expired verses.
                self.__objects = {}
                return None

            return verse
        except KeyError:
            return None

    def reload(self) -> None:
        """Read the storage file and load daily verses"""

        try:
            with open(self.__file_path, "r") as f:
                content: dict[str, dict[str, Any]] = json.load(f)

            self.__objects = {
                key: DailyVerse(**value) for key, value in content.items()
            }

        except FileNotFoundError:
            pass

        except json.decoder.JSONDecodeError:
            pass

        if not self.__objects and not self.__reference:
            # daily verse not yet generated
            self.__todays_verse()
        elif not self.__reference:
            # set reference from one of the objects
            self.__reference = list(self.__objects.values())[0].reference

    def new(
        self,
        bible_version: Version,
        verse_text: list[str],
        save: bool = False,
    ) -> DailyVerse:
        """Add new daily verse using given bible version.

        Args:
            bible_version (Version): Bible version.
            verse_text (list[str]): list of verses.
            save (bool, optional): If set to True, write the resulting objects
                to file. Defaults to False.

        Returns:
            DailyVerse: the new daily verse
        """

        todays_verse = DailyVerse(
            reference=self.__reference,
            verse_text=verse_text,
            bible_version=bible_version.title,
            day=date.today(),
        )

        self.__objects[bible_version.value] = todays_verse

        if save:
            self.save()

        return todays_verse

    def save(self) -> None:
        """Write the objects to file"""

        try:
            with open(self.__file_path, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        key: value.model_dump(mode="json")
                        for key, value in self.__objects.items()
                    },
                    f,
                    indent=2,
                )
        except Exception:
            pass

    def _is_expired(self, verse: DailyVerse) -> bool:
        """Check if the daily verse is past its creation date.

        Args:
            verse (DailyVerse): daily verse to check

        Returns:
            bool: `True` if the verse is not valid for today, else `False`.
        """
        return verse.day != date.today()
