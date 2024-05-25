from pythonbible import BookGroup

SHORT_VERSION_NAMES = ["NIV", "ASV", "KJV"]

MAPPED_BOOK_GROUPS = {
    # All books
    "Any": None,
    # Testaments
    "Old Testament": BookGroup.OLD_TESTAMENT,
    "New Testament": BookGroup.NEW_TESTAMENT,
    # Smaller groups
    "Law": BookGroup.OLD_TESTAMENT_LAW,
    "History": BookGroup.OLD_TESTAMENT_HISTORY,
    "Poetry": BookGroup.OLD_TESTAMENT_POETRY_WISDOM,
    "Wisdom": BookGroup.OLD_TESTAMENT_POETRY_WISDOM,
    "Prophecy": BookGroup.OLD_TESTAMENT_PROPHECY,
    "Major Prophets": BookGroup.OLD_TESTAMENT_MAJOR_PROPHETS,
    "Minor Prophets": BookGroup.OLD_TESTAMENT_MINOR_PROPHETS,
    "Gospels": BookGroup.NEW_TESTAMENT_GOSPELS,
    "Epistles": BookGroup.NEW_TESTAMENT_EPISTLES,
    "Paul Epistles": BookGroup.NEW_TESTAMENT_PAUL_EPISTLES,
    "General Epistles": BookGroup.NEW_TESTAMENT_GENERAL_EPISTLES,
    "Apocalyptic": BookGroup.NEW_TESTAMENT_APOCALYPTIC,
}

DAILY_VERSE_FILE = "daily_verse.json"
