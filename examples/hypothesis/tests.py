import string
import unittest
from decimal import Decimal

from fake import FAKER, FILE_REGISTRY, StringValue, slugify
from hypothesis import Verbosity, given, settings, strategies as st

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("TestFakerWithHypothesis",)

# Enable verbose logging for all tests in the class
settings.register_profile("debug", verbosity=Verbosity.verbose)
settings.load_profile("debug")


class TestFakerWithHypothesis(unittest.TestCase):
    """Test `fake.Faker` with hypothesis."""

    def setUp(self) -> None:
        self.faker = FAKER

    def tearDown(self) -> None:
        FILE_REGISTRY.clean_up()

    @given(st.text(min_size=5))
    def test_slugify(self, value):
        result = slugify(f"{value}a1")

        # Check that the result is lowercased
        self.assertEqual(result, result.lower())

        # Check that the result does not contain any punctuation or whitespace
        for char in string.punctuation + string.whitespace:
            self.assertNotIn(char, result)

        # Check that the result is an alpha-numeric string (since all
        # punctuations and whitespaces are removed)
        self.assertTrue(result.isalnum())

    @given(nb=st.integers(min_value=1, max_value=10))
    def test_words(self, nb):
        words = self.faker.words(nb=nb)
        self.assertIsInstance(words, list)
        self.assertEqual(len(words), nb)

    @given(nb_words=st.integers(min_value=1, max_value=10))
    def test_sentence(self, nb_words):
        sentence = self.faker.sentence(nb_words=nb_words)
        self.assertIsInstance(sentence, str)
        self.assertTrue(len(sentence.split()) == nb_words)

    @given(nb=st.integers(min_value=1, max_value=10))
    def test_sentences(self, nb):
        sentences = self.faker.sentences(nb=nb)
        self.assertIsInstance(sentences, list)
        self.assertEqual(len(sentences), nb)

    @given(nb_sentences=st.integers(min_value=1, max_value=10))
    def test_paragraph(self, nb_sentences):
        paragraph = self.faker.paragraph(nb_sentences=nb_sentences)
        self.assertIsInstance(paragraph, str)

    @given(nb=st.integers(min_value=1, max_value=10))
    def test_paragraphs(self, nb):
        paragraphs = self.faker.paragraphs(nb=nb)
        self.assertIsInstance(paragraphs, list)
        self.assertEqual(len(paragraphs), nb)

    @given(nb_chars=st.integers(min_value=1, max_value=1000))
    def test_text(self, nb_chars):
        text = self.faker.text(nb_chars=nb_chars)
        self.assertIsInstance(text, str)
        self.assertTrue(len(text) <= nb_chars)

    @given(nb=st.integers(min_value=1, max_value=10))
    def test_texts(self, nb):
        texts = self.faker.texts(nb=nb)
        self.assertIsInstance(texts, list)
        self.assertEqual(len(texts), nb)

    @given(
        min_val=st.floats(
            min_value=-1e10,
            max_value=1e10,
            allow_nan=False,
            allow_infinity=False,
        ),
        max_val=st.floats(
            min_value=-1e10,
            max_value=1e10,
            allow_nan=False,
            allow_infinity=False,
        ),
    )
    def test_pyfloat(self, min_val, max_val):
        if min_val > max_val:
            min_val, max_val = max_val, min_val
        val = self.faker.pyfloat(min_value=min_val, max_value=max_val)
        self.assertIsInstance(val, float)
        self.assertGreaterEqual(val, min_val)
        self.assertLessEqual(val, max_val)

    @given(
        left_digits=st.integers(min_value=0, max_value=10),
        right_digits=st.integers(min_value=0, max_value=10),
        positive=st.booleans(),
    )
    def test_pydecimal(self, left_digits, right_digits, positive):
        decimal_number = self.faker.pydecimal(
            left_digits=left_digits,
            right_digits=right_digits,
            positive=positive,
        )
        self.assertIsInstance(decimal_number, Decimal)

    @given(nb_pages=st.integers(min_value=1, max_value=10))
    def test_pdf(self, nb_pages):
        pdf_bytes = self.faker.pdf(nb_pages=nb_pages)
        self.assertIsInstance(pdf_bytes, bytes)

    @given(
        size=st.tuples(
            st.integers(min_value=1, max_value=500),
            st.integers(min_value=1, max_value=500),
        ),
        color=st.tuples(
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
        ),
    )
    def test_png(self, size, color):
        png_bytes = self.faker.png(size=size, color=color)
        self.assertIsInstance(png_bytes, bytes)

    @given(
        size=st.tuples(
            st.integers(min_value=1, max_value=500),
            st.integers(min_value=1, max_value=500),
        ),
        color=st.tuples(
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
        ),
    )
    def test_svg(self, size, color):
        svg_bytes = self.faker.svg(size=size, color=color)
        self.assertIsInstance(svg_bytes, bytes)

    @given(
        size=st.tuples(
            st.integers(min_value=1, max_value=500),
            st.integers(min_value=1, max_value=500),
        ),
        color=st.tuples(
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
        ),
    )
    def test_bmp(self, size, color):
        bmp_bytes = self.faker.bmp(size=size, color=color)
        self.assertIsInstance(bmp_bytes, bytes)

    @given(
        size=st.tuples(
            st.integers(min_value=1, max_value=500),
            st.integers(min_value=1, max_value=500),
        ),
        color=st.tuples(
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
        ),
    )
    def test_gif(self, size, color):
        gif_bytes = self.faker.gif(size=size, color=color)
        self.assertIsInstance(gif_bytes, bytes)

    @given(nb_pages=st.integers(min_value=1, max_value=10))
    def test_docx(self, nb_pages):
        docx_bytes = self.faker.docx(nb_pages=nb_pages)
        self.assertIsInstance(docx_bytes, bytes)

    @given(nb_pages=st.integers(min_value=1, max_value=10))
    def test_pdf_file(self, nb_pages):
        pdf_file = self.faker.pdf_file(nb_pages=nb_pages)
        self.assertIsInstance(pdf_file, StringValue)

    @given(
        size=st.tuples(
            st.integers(min_value=1, max_value=500),
            st.integers(min_value=1, max_value=500),
        ),
        color=st.tuples(
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
        ),
    )
    def test_png_file(self, size, color):
        png_file = self.faker.png_file(size=size, color=color)
        self.assertIsInstance(png_file, StringValue)

    @given(
        size=st.tuples(
            st.integers(min_value=1, max_value=500),
            st.integers(min_value=1, max_value=500),
        ),
        color=st.tuples(
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
        ),
    )
    def test_svg_file(self, size, color):
        svg_file = self.faker.svg_file(size=size, color=color)
        self.assertIsInstance(svg_file, StringValue)

    @given(
        size=st.tuples(
            st.integers(min_value=1, max_value=500),
            st.integers(min_value=1, max_value=500),
        ),
        color=st.tuples(
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
        ),
    )
    def test_bmp_file(self, size, color):
        bmp_file = self.faker.bmp_file(size=size, color=color)
        self.assertIsInstance(bmp_file, StringValue)

    @given(
        size=st.tuples(
            st.integers(min_value=1, max_value=500),
            st.integers(min_value=1, max_value=500),
        ),
        color=st.tuples(
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
            st.integers(min_value=0, max_value=255),
        ),
    )
    def test_gif_file(self, size, color):
        gif_file = self.faker.gif_file(size=size, color=color)
        self.assertIsInstance(gif_file, StringValue)

    @given(nb_pages=st.integers(min_value=1, max_value=10))
    def test_docx_file(self, nb_pages):
        docx_file = self.faker.docx_file(nb_pages=nb_pages)
        self.assertIsInstance(docx_file, StringValue)

    @given(nb_chars=st.integers(min_value=1, max_value=1000))
    def test_txt_file(self, nb_chars):
        txt_file = self.faker.txt_file(nb_chars=nb_chars)
        self.assertIsInstance(txt_file, StringValue)


if __name__ == "__main__":
    unittest.main()
