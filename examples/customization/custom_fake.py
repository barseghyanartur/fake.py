import random
import string

from fake import Factory, Faker

__all__ = (
    "FACTORY",
    "FAKER",
)

# Custom first names dictionary
FIRST_NAMES = [
    "Anahit",
    "Ani",
    "Aram",
    "Areg",
    "Artur",
    "Astghik",
    "Barsegh",
    "Gaiane",
    "Gor",
    "Hakob",
    "Hasmik",
    "Levon",
    "Lilit",
    "Mariam",
    "Narek",
    "Nune",
    "Tatev",
    "Tigran",
    "Vahan",
    "Vardan",
    "Zara",
]

# Custom last names dictionary
LAST_NAMES = [
    "Amatouni",
    "Avagyan",
    "Danielyan",
    "Gevorgyan",
    "Gnouni",
    "Grigoryan",
    "Hakobyan",
    "Harutyunyan",
    "Hovhannisyan",
    "Karapetyan",
    "Khachatryan",
    "Manukyan",
    "Ter-Martirosyan",
    "Melikyan",
    "Mkrtchyan",
    "Petrosyan",
    "Saroyan",
    "Sahakyants",
    "Sargsyan",
    "Sedrakyan",
    "Simonyan",
    "Stepanyan",
    "Vardanyan",
]

# Custom words dictionary
WORDS = [
    "time",
    "person",
    "year",
    "way",
    "day",
    "thing",
    "man",
    "world",
    "life",
    "hand",
    "part",
    "child",
    "eye",
    "woman",
    "place",
    "work",
    "week",
    "case",
    "point",
    "government",
    "company",
    "number",
    "group",
    "problem",
    "fact",
    "be",
    "have",
    "do",
    "say",
    "get",
    "make",
    "go",
    "know",
    "take",
    "see",
    "come",
    "think",
    "look",
    "want",
    "give",
    "use",
    "find",
    "tell",
    "ask",
    "work",
    "seem",
    "feel",
    "try",
    "leave",
    "call",
    "good",
    "new",
    "first",
    "last",
    "long",
    "great",
    "little",
    "own",
    "other",
    "old",
    "right",
    "big",
    "high",
    "different",
    "small",
    "large",
    "next",
    "early",
    "young",
    "important",
    "few",
    "public",
    "bad",
    "same",
    "able",
    "to",
    "of",
    "in",
    "for",
    "on",
    "with",
    "as",
    "at",
    "by",
    "from",
    "up",
    "about",
    "into",
    "over",
    "after",
    "beneath",
    "under",
    "above",
    "the",
    "and",
    "a",
    "that",
    "I",
    "it",
    "not",
]


class CustomFaker(Faker):
    """Custom Faker class."""

    def load_names(self) -> None:
        """Override default first- and last-names dictionaries."""
        self._first_names = FIRST_NAMES
        self._last_names = LAST_NAMES

    def load_words(self) -> None:
        """Override default words dictionary."""
        self._words = WORDS

    def postal_code(self) -> str:
        """Generate a random Dutch postal code in the format '1234 AB'.

        :return: A randomly generated Dutch postal code as a string.
        """
        number_part = "".join(random.choices(string.digits, k=4))
        letter_part = "".join(random.choices(string.ascii_uppercase, k=2))
        return f"{number_part} {letter_part}"


FAKER = CustomFaker()
FACTORY = Factory(FAKER)
