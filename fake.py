"""
https://github.com/barseghyanartur/fake.py/
"""

import contextlib
import io
import os
import random
import re
import string
import unittest
import zlib
from datetime import date, datetime, timedelta
from tempfile import NamedTemporaryFile
from typing import Dict, List, Literal, Optional, Set, Tuple, Type, Union

__title__ = "fake.py"
__version__ = "0.1"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("Faker",)


PDF_TEXT_TPL_PAGE_OBJECT = """{page_num} 0 obj
<</Type /Page
/Parent 3 0 R
/Resources 2 0 R
/Contents {content_obj_num} 0 R
>>
endobj
"""

PDF_TEXT_TPL_CONTENT_OBJECT = """{obj_num} 0 obj
<</Length {stream_length}>>
stream
{content}
endstream
endobj
"""

PDF_GRAPHIC_TPL_IMAGE_OBJECT = """{obj_num} 0 obj
<</Type /XObject
/Subtype /Image
/Width {width}
/Height {height}
/ColorSpace /DeviceRGB
/BitsPerComponent 8
/Filter /FlateDecode
/Length {stream_length}>>
stream
"""

PDF_GRAPHIC_TPL_PAGE_OBJECT = """{page_obj_num} 0 obj
<</Type /Page
/Parent 3 0 R
/Resources <</XObject <</Im{image_obj_num} {image_obj_num} 0 R>> >>
/Contents {content_obj_num} 0 R
>>
endobj
"""

PDF_GRAPHIC_TPL_CONTENT_OBJECT = """{content_obj_num} 0 obj
<</Length 44>>
stream
q
100 0 0 100 0 0 cm
/Im{image_obj_num} Do
Q
endstream
endobj
"""

PDF_GRAPHIC_TPL_PAGES_OBJECT = """3 0 obj
<</Type /Pages
/Kids [{pages_kids}]
/Count {num_pages}
>>
endobj
"""

PDF_GRAPHIC_TPL_CATALOG_OBJECT = """1 0 obj
<</Type /Catalog
/Pages 3 0 R
>>
endobj
"""

PDF_GRAPHIC_TPL_TRAILER_OBJECT = """trailer
<</Size 6
/Root 1 0 R>>
startxref
"""

SVG_TPL = """
<svg width="{width}px" height="{height}px" xmlns="http://www.w3.org/2000/svg">
<rect width="100%" height="100%" fill="rgb{color}" />
</svg>"""


class TextPdfGenerator:
    """Text PDF generatr.

    Usage example:

    .. code-block:: python

        from pathlib import Path
        from faker import Faker, TextPdfGenerator

        FAKER = Faker()

        text_pdf_file = Path("media") / "text_pdf.pdf"
        text_pdf_file.write_bytes(
            FAKER.pdf(nb_pages=100, generator=TextPdfGenerator)
        )
    """

    nb_pages: int
    texts: List[str]

    def __init__(self, faker: "Faker"):
        self.faker = faker

    def _add_page_object(self, page_num, content_obj_num):
        return PDF_TEXT_TPL_PAGE_OBJECT.format(
            page_num=page_num,
            content_obj_num=content_obj_num,
        )

    def _add_content_object(self, obj_num, page_text):
        content = f"BT /F1 24 Tf 100 700 Td ({page_text}) Tj ET"
        stream_length = len(content)
        return PDF_TEXT_TPL_CONTENT_OBJECT.format(
            obj_num=obj_num,
            stream_length=stream_length,
            content=content,
        )

    def create(
        self,
        nb_pages: Optional[int] = None,
        texts: Optional[List[str]] = None,
    ) -> bytes:
        # Initialization
        if not nb_pages and not texts:
            raise ValueError(
                "Either `num_pages` or `texts` arguments shall be given."
            )
        if texts:
            self.nb_pages: int = len(texts)
            self.texts = texts
        else:
            self.nb_pages: int = nb_pages or 1
            self.texts = self.faker.sentences(nb=self.nb_pages)

        # Construction
        pdf_bytes = io.BytesIO()

        pdf_bytes.write(b"%PDF-1.0\n")
        pdf_bytes.write(b"1 0 obj\n<</Type /Catalog/Pages 3 0 R>>\nendobj\n")
        pdf_bytes.write(
            b"2 0 obj\n<</Font <</F1 <</Type /Font/Subtype /Type1/BaseFont "
            b"/Helvetica>>>>\nendobj\n"
        )
        pdf_bytes.write(b"3 0 obj\n<</Type /Pages/Kids [")

        page_objs = []
        content_objs = []
        for i, page_text in enumerate(self.texts):
            page_obj_num = 4 + 2 * i
            content_obj_num = page_obj_num + 1
            # page_text = f"Page {i + 1}: {text}"
            page_objs.append(
                self._add_page_object(page_obj_num, content_obj_num)
            )
            content_objs.append(
                self._add_content_object(content_obj_num, page_text)
            )
            pdf_bytes.write(f"{page_obj_num} 0 R ".encode())

        pdf_bytes.write(f"] /Count {str(self.nb_pages)}>>\nendobj\n".encode())

        for page_obj in page_objs:
            pdf_bytes.write(page_obj.encode())
        for content_obj in content_objs:
            pdf_bytes.write(content_obj.encode())

        pdf_bytes.write(f"xref\n0 {str(4 + 2 * self.nb_pages)}\n".encode())
        pdf_bytes.write(b"0000000000 65535 f \n")
        pdf_bytes.write(
            b"0000000010 00000 n \n0000000057 00000 n \n0000000103 00000 n \n"
        )
        offset = 149
        for i in range(self.nb_pages):
            pdf_bytes.write(f"{offset:010} 00000 n \n".encode())
            offset += 78
            pdf_bytes.write(f"{offset:010} 00000 n \n".encode())
            offset += 73

        pdf_bytes.write(
            f"trailer\n<</Size {str(4 + 2 * self.nb_pages)}/Root 1 0 R>>\n"
            f"".encode()
        )
        pdf_bytes.write(b"startxref\n564\n%%EOF")

        return pdf_bytes.getvalue()


class GraphicPdfGenerator:
    """Graphic PDF generatr.

    Usage example:

    .. code-block:: python

        from pathlib import Path
        from faker import Faker, GraphicPdfGenerator

        FAKER = Faker()

        graphic_pdf_file = Path("media") / "graphic_pdf.pdf"
        graphic_pdf_file.write_bytes(
            FAKER.pdf(nb_pages=100, generator=GraphicPdfGenerator)
        )
    """

    nb_pages: int
    image_size: Tuple[int, int]
    image_color: Tuple[int, int, int]

    def __init__(self, faker: "Faker"):
        self.faker = faker

    def _create_raw_image_data(self):
        width, height = self.image_size
        # Create uncompressed raw RGB data
        raw_data = bytes(self.image_color) * width * height
        return zlib.compress(raw_data)

    def _add_image_object(self, pdf_bytes, obj_num):
        width, height = self.image_size
        image_stream = self._create_raw_image_data()
        stream_length = len(image_stream)
        pdf_bytes.write(
            PDF_GRAPHIC_TPL_IMAGE_OBJECT.format(
                obj_num=obj_num,
                width=width,
                height=height,
                stream_length=stream_length,
            ).encode()
        )
        pdf_bytes.write(image_stream)
        pdf_bytes.write(b"\nendstream\nendobj\n")

    def create(
        self,
        nb_pages: int = 1,
        image_size: Tuple[int, int] = (100, 100),
        image_color: Tuple[int, int, int] = (255, 0, 0),
    ) -> bytes:
        # Initialization
        self.nb_pages = nb_pages
        self.image_size = image_size
        self.image_color = image_color

        # Construction
        pdf_bytes = io.BytesIO()
        pdf_bytes.write(b"%PDF-1.0\n")

        # Image object number
        image_obj_num = 4

        # Positions in the PDF for the xref table
        positions = [pdf_bytes.tell()]

        # Add image object
        self._add_image_object(pdf_bytes, image_obj_num)
        positions.append(pdf_bytes.tell())

        # Add pages
        for i in range(self.nb_pages):
            page_obj_num = 5 + i
            content_obj_num = page_obj_num + self.nb_pages
            pdf_bytes.write(
                PDF_GRAPHIC_TPL_PAGE_OBJECT.format(
                    page_obj_num=page_obj_num,
                    image_obj_num=image_obj_num,
                    content_obj_num=content_obj_num,
                ).encode()
            )
            positions.append(pdf_bytes.tell())

            # Content stream that uses the image
            pdf_bytes.write(
                PDF_GRAPHIC_TPL_CONTENT_OBJECT.format(
                    content_obj_num=content_obj_num,
                    image_obj_num=image_obj_num,
                ).encode()
            )
            positions.append(pdf_bytes.tell())

        # Pages object
        pages_kids = " ".join([f"{5 + i} 0 R" for i in range(self.nb_pages)])
        pdf_bytes.write(
            PDF_GRAPHIC_TPL_PAGES_OBJECT.format(
                pages_kids=pages_kids,
                num_pages=self.nb_pages,
            ).encode()
        )
        positions.append(pdf_bytes.tell())

        # Catalog object
        pdf_bytes.write(PDF_GRAPHIC_TPL_CATALOG_OBJECT.encode())
        positions.append(pdf_bytes.tell())

        # xref table
        pdf_bytes.write(b"xref\n0 1\n0000000000 65535 f \n")
        for pos in positions:
            pdf_bytes.write(f"{pos:010} 00000 n \n".encode())

        # Trailer
        pdf_bytes.write(PDF_GRAPHIC_TPL_TRAILER_OBJECT.encode())
        pdf_bytes.write(f"{positions[-1]}\n".encode())
        pdf_bytes.write(b"%%EOF")

        return pdf_bytes.getvalue()


class AuthorshipData:
    _authorship_data: Dict[str, List[str]] = {}
    first_names: Set[str] = set()
    last_names: Set[str] = set()

    def _find_authorship_info(self, file_path: str) -> List[str]:
        authorship_info = []
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    if "__author__" in line or "Author:" in line:
                        authorship_info.append(line.strip())
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as file:
                for line in file:
                    if "__author__" in line or "Author:" in line:
                        authorship_info.append(line.strip())
        return authorship_info

    def _extract_authorship_info_from_stdlib(self) -> None:
        stdlib_path = os.path.dirname(os.__file__)

        for root, dirs, files in os.walk(stdlib_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    authorship_info = self._find_authorship_info(file_path)
                    if authorship_info:
                        self._authorship_data[file_path] = authorship_info

    def _extract_names(self) -> None:
        """Extract first and last names from authorship information.
        Ensures that multi-part last names are treated as a single entity.
        """
        # Patterns for different cases
        patterns = {
            # For simple cases like '# Author: <author>'
            "simple": r"# Author: ([\w\s\-\']+)",
            # For cases like '__author__ = "<author> <email>"'
            "email_in_brackets": r'__author__\s*=\s*"([\w\s\-\']+)',
            # For multiple authors like '# Author: <author>, <author>'
            "multiple_authors": r"# Author: ([\w\s\-\']+), ([\w\s\-\']+)",
            # For cases like '# Author: <author>, <email>'
            "author_with_email": r"# Author: ([\w\s\-\']+), \w+@[\w\.-]+",
        }

        for info_list in self._authorship_data.values():
            for info in info_list:
                # Ignoring anything after '--', emails, and dates
                info = re.sub(
                    (
                        r"--.*|<[\w\.-]+@[\w\.-]+>|\b\d{4}\b|\bJanuary\b|"
                        r"\bFebruary\b|\bMarch\b|\bApril\b|\bMay\b|\bJune\b|"
                        r"\bJuly\b|\bAugust\b|\bSeptember\b|\bOctober\b|"
                        r"\bNovember\b|\bDecember\b"
                    ),
                    "",
                    info,
                )

                for pattern in patterns.values():
                    found_names = re.findall(pattern, info)
                    for name in found_names:
                        if isinstance(name, tuple):
                            # In case of multiple authors
                            for n in name:
                                split_name = n.strip().split()
                                if len(split_name) >= 2:
                                    if split_name[0] not in {"The"}:
                                        self.first_names.add(split_name[0])
                                    self.last_names.add(
                                        " ".join(split_name[1:])
                                    )  # Joining multi-part last names
                        else:
                            split_name = name.strip().split()
                            if len(split_name) >= 2:
                                if split_name[0] not in {"The"}:
                                    self.first_names.add(split_name[0])
                                self.last_names.add(
                                    " ".join(split_name[1:])
                                )  # Joining multi-part last names

    def __init__(self):
        self._extract_authorship_info_from_stdlib()
        self._extract_names()


class Faker:
    """faker.py - simplified, standalone alternative with no dependencies.

    ----

    Usage example:

    .. code-block:: python

        from faker import Faker

        FAKER = Faker()

        print(FAKER.first_name())  # Random first name
        print(FAKER.last_name())  # Random last name
        print(FAKER.name())  # Random name
        print(FAKER.word())  # Random word from the Zen of Python
        print(FAKER.words(nb=3))  # List of 3 random words from Zen of Python
        print(FAKER.sentence())  # Random sentence (5 random words by default)
        print(FAKER.paragraph())  # Paragraph (5 random sentences by default)
        print(FAKER.paragraphs())  # 3 random paragraphs
        print(FAKER.text())  # Random text up to 200 characters
        print(FAKER.file_name())  # Random filename with '.txt' extension
        print(FAKER.email())  # Random email
        print(FAKER.url())  # Random URL
        print(FAKER.pyint())  # Random integer
        print(FAKER.pybool())  # Random boolean
        print(FAKER.pystr())  # Random string
        print(FAKER.pyfloat())  # Random float

    ----

    PDF:

    .. code-block:: python

        from pathlib import Path
        from faker import Faker, TextPdfGenerator, GraphicPdfGenerator

        FAKER = Faker()

        graphic_pdf_file = Path("media") / "graphic_pdf.pdf"
        graphic_pdf_file.write_bytes(
            FAKER.pdf(num_pages=100, generator=GraphicPdfGenerator)
        )

        text_pdf_file = Path("media") / "text_pdf.pdf"
        text_pdf_file.write_bytes(
            FAKER.pdf(num_pages=100, generator=TextPdfGenerator)
        )

    ----

    Various image formats:

    .. code-block:: python

        from pathlib import Path
        from faker import Faker, TextPdfGenerator, GraphicPdfGenerator

        FAKER = Faker()

        png_file = Path("media") / "image.png"
        png_file.write_bytes(FAKER.png())

        svg_file = Path("media") / "image.svg"
        svg_file.write_bytes(FAKER.svg())

        bmp_file = Path("media") / "image.bmp"
        bmp_file.write_bytes(FAKER.bmp())

        gif_file = Path("media") / "image.gif"
        gif_file.write_bytes(FAKER.gif())

    Note, that all image formats accept `size` (default: `(100, 100)`)
    and `color`(default: `(255, 0, 0)`) arguments.
    """

    def __init__(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            # Dynamically import 'this' module
            this = __import__("this")

        zen_encoded: str = this.s
        translation_map: Dict[str, str] = {v: k for k, v in this.d.items()}
        zen: str = self._rot13_translate(zen_encoded, translation_map)
        self._words: List[str] = (
            zen.translate(str.maketrans("", "", string.punctuation))
            .lower()
            .split()
        )
        self._authorship_data = AuthorshipData()
        self._first_names = list(self._authorship_data.first_names)
        self._last_names = list(self._authorship_data.last_names)

    @staticmethod
    def _rot13_translate(text: str, translation_map: Dict[str, str]) -> str:
        return "".join([translation_map.get(c, c) for c in text])

    def first_name(self) -> str:
        return random.choice(self._first_names)

    def last_name(self) -> str:
        return random.choice(self._last_names)

    def name(self) -> str:
        return f"{self.first_name()} {self.last_name()}"

    def word(self) -> str:
        return random.choice(self._words).capitalize()

    def words(self, nb: int = 5) -> List[str]:
        return [word.capitalize() for word in random.choices(self._words, k=nb)]

    def sentence(self, nb_words: int = 5) -> str:
        return (
            f"{' '.join([self.word() for _ in range(nb_words)]).capitalize()}."
        )

    def sentences(self, nb: int = 3) -> List[str]:
        return [self.sentence() for _ in range(nb)]

    def paragraph(self, nb_sentences: int = 5) -> str:
        return " ".join([self.sentence() for _ in range(nb_sentences)])

    def paragraphs(self, nb: int = 3) -> List[str]:
        return [self.paragraph() for _ in range(nb)]

    def text(self, nb_chars: int = 200) -> str:
        current_text: str = ""
        while len(current_text) < nb_chars:
            sentence: str = self.sentence()
            current_text += f" {sentence}" if current_text else sentence
        return current_text[:nb_chars]

    def file_name(self, extension: str = "txt") -> str:
        with NamedTemporaryFile(suffix=f".{extension}") as temp_file:
            return temp_file.name

    def email(self, domain: str = "example.com") -> str:
        if not domain:
            domain = "example.com"
        return f"{self.word().lower()}@{domain}"

    def url(
        self,
        protocols: Optional[Tuple[str]] = None,
        tlds: Optional[Tuple[str]] = None,
        suffixes: Optional[Tuple[str]] = None,
    ) -> str:
        protocol = random.choice(protocols or ("http", "https"))
        domain = self.word().lower()
        tld = random.choice(
            tlds
            or (
                "com",
                "org",
                "net",
                "io",
            )
        )
        suffix = random.choice(suffixes or (".html", ".php", ".go", "", "/"))
        return f"{protocol}://{domain}.{tld}/{self.word().lower()}{suffix}"

    def pyint(self, min_value: int = 0, max_value: int = 9999) -> int:
        return random.randint(min_value, max_value)

    def pybool(self) -> bool:
        return random.choice(
            (
                True,
                False,
            )
        )

    def pystr(self, nb_chars: int = 20) -> str:
        return "".join(random.choices(string.ascii_letters, k=nb_chars))

    def pyfloat(
        self,
        min_value: float = 0.0,
        max_value: float = 10.0,
    ) -> float:
        return random.uniform(min_value, max_value)

    def ipv4(self) -> str:
        return ".".join(str(random.randint(0, 255)) for _ in range(4))

    def _parse_date_string(self, date_str: str) -> datetime:
        """Parse date string with notation below into a datetime object:

        - '5M': 5 minutes from now
        - '-1d': 1 day ago
        - '-1H': 1 hour ago
        - '-365d': 365 days ago

        :param date_str: The date string with shorthand notation.
        :return: A datetime object representing the time offset.
        """
        if date_str in ["now", "today"]:
            return datetime.now()

        match = re.match(r"([+-]?\d+)([dHM])", date_str)
        if not match:
            raise ValueError(
                "Date string format is incorrect. Expected formats like "
                "'-1d', '+2H', '-30M'."
            )
        value, unit = match.groups()
        value = int(value)
        if unit == "d":  # Days
            return datetime.now() + timedelta(days=value)
        elif unit == "H":  # Hours
            return datetime.now() + timedelta(hours=value)
        elif unit == "M":  # Minutes
            return datetime.now() + timedelta(minutes=value)
        else:
            raise ValueError(
                "Date string format is incorrect. Expected formats like "
                "'-1d', '+2H', '-30M'."
            )

    def date_between(
        self,
        start_date: str,
        end_date: str = "+0d",
    ) -> date:
        """Generate random date between `start_date` and `end_date`.

        :param start_date: The start date from which the random date should
            be generated in the shorthand notation.
        :param end_date: The end date up to which the random date should be
            generated in the shorthand notation.
        :return: A string representing the formatted date.
        """
        start_datetime = self._parse_date_string(start_date)
        end_datetime = self._parse_date_string(end_date)
        time_between_dates = (end_datetime - start_datetime).days
        random_days = random.randrange(
            time_between_dates + 1
        )  # Include the end date
        random_date = start_datetime + timedelta(days=random_days)
        return random_date.date()

    def date_time_between(
        self,
        start_date: str,
        end_date: str = "+0d",
    ) -> datetime:
        """Generate a random datetime between `start_date` and `end_date`.

        :param start_date: The start datetime from which the random datetime
            should be generated in the shorthand notation.
        :param end_date: The end datetime up to which the random datetime
            should be generated in the shorthand notation.
        :return: A string representing the formatted datetime.
        """
        start_datetime = self._parse_date_string(start_date)
        end_datetime = self._parse_date_string(end_date)
        time_between_datetimes = int(
            (end_datetime - start_datetime).total_seconds()
        )
        random_seconds = random.randrange(
            time_between_datetimes + 1
        )  # Include the end date time
        random_date_time = start_datetime + timedelta(seconds=random_seconds)
        return random_date_time

    def pdf(
        self,
        nb_pages: int = 1,
        generator: Union[
            Type[TextPdfGenerator], Type[GraphicPdfGenerator]
        ] = GraphicPdfGenerator,
        **kwargs,
    ) -> bytes:
        """Create a PDF document of a given size."""
        _pdf = generator(faker=self)
        return _pdf.create(nb_pages=nb_pages, **kwargs)

    def png(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
    ) -> bytes:
        """Create a PNG image of a specified color.

        :param size: Tuple of width and height of the image in pixels.
        :param color: Color of the image in RGB format (tuple of three
            integers).
        :return: Byte content of the PNG image.
        """
        width, height = size

        # PNG file format header
        png_header = b"\x89PNG\r\n\x1a\n"

        # IHDR chunk: width, height, bit depth, color type, compression,
        # filter, interlace
        ihdr_content = (
            width.to_bytes(4, byteorder="big")
            + height.to_bytes(4, byteorder="big")
            + b"\x08\x02\x00\x00\x00"
        )
        ihdr = b"IHDR" + ihdr_content
        ihdr_chunk = (
            len(ihdr_content).to_bytes(4, byteorder="big")
            + ihdr
            + zlib.crc32(ihdr).to_bytes(4, byteorder="big")
        )

        # IDAT chunk: image data
        raw_data = (
            b"\x00" + bytes(color) * width
        )  # No filter, and RGB data for each pixel
        compressed_data = zlib.compress(raw_data * height)  # Compress the data
        idat_chunk = (
            len(compressed_data).to_bytes(4, byteorder="big")
            + b"IDAT"
            + compressed_data
            + zlib.crc32(b"IDAT" + compressed_data).to_bytes(
                length=4, byteorder="big"
            )
        )

        # IEND chunk: marks the image end
        iend_chunk = b"\x00\x00\x00\x00IEND\xAE\x42\x60\x82"

        # Combine all chunks
        png_data = png_header + ihdr_chunk + idat_chunk + iend_chunk

        return png_data

    def svg(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
    ) -> bytes:
        """Create a SVG image of a specified color.

        :param size: Tuple of width and height of the image in pixels.
        :param color: Color of the image in RGB format (tuple of three
            integers).
        :return: Byte content of the SVG image.
        """
        width, height = size
        return SVG_TPL.format(width=width, height=height, color=color).encode()

    def bmp(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
    ) -> bytes:
        """Create a BMP image of a specified color.

        :param size: Tuple of width and height of the image in pixels.
        :param color: Color of the image in RGB format (tuple of three
            integers).
        :return: Byte content of the BMP image.
        """
        width, height = size

        # BMP Header and DIB Header (BITMAPINFOHEADER format)
        file_header = b"BM"  # Signature
        dib_header = b"\x28\x00\x00\x00"  # DIB Header size (40 bytes)

        # Image width and height
        width_bytes = width.to_bytes(4, byteorder="little")
        height_bytes = height.to_bytes(4, byteorder="little")

        # Image pixel data
        # BMP files are padded to be a multiple of 4 bytes wide
        row_padding = (4 - (3 * width) % 4) % 4
        pixel_data = bytes(color[::-1]) * width + b"\x00" * row_padding
        image_data = pixel_data * height

        # File size
        file_size = (
            14 + 40 + len(image_data)
        )  # 14 bytes file header, 40 bytes DIB header
        file_size_bytes = file_size.to_bytes(4, byteorder="little")

        # Final assembly of the BMP file
        return (
            file_header
            + file_size_bytes
            + b"\x00\x00\x00\x00"
            + b"\x36\x00\x00\x00"  # Reserved 4 bytes
            # Pixel data offset (54 bytes: 14 for file header, 40 for DIB
            # header)
            + dib_header
            + width_bytes
            + height_bytes
            + b"\x01\x00"
            + b"\x18\x00"  # Number of color planes
            + b"\x00\x00\x00\x00"  # Bits per pixel (24 for RGB)
            + len(image_data).to_bytes(  # Compression method (0 for none)
                4, byteorder="little"
            )
            + b"\x13\x0B\x00\x00"  # Size of the raw bitmap data
            # Print resolution of the image (2835 pixels/meter)
            + b"\x13\x0B\x00\x00"
            + b"\x00\x00\x00\x00"
            + b"\x00\x00\x00\x00"  # Number of colors in the palette
            + image_data  # Important colors
        )

    def gif(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
    ) -> bytes:
        """Create a GIF image of a specified color.

        :param size: Tuple of width and height of the image in pixels.
        :param color: Color of the image in RGB format (tuple of three
            integers).
        :return: Byte content of the GIF image.
        """
        width, height = size

        # Header
        header = b"GIF89a"

        # Logical Screen Descriptor
        screen_width = width.to_bytes(2, byteorder="little")
        screen_height = height.to_bytes(2, byteorder="little")
        # Global Color Table Flag set to 1, Color resolution, and Sort Flag
        # to 0
        packed_field = b"\xF7"
        bg_color_index = b"\x00"  # Background Color Index
        pixel_aspect_ratio = b"\x00"  # No aspect ratio information

        # Global Color Table.
        # Since it's a single color, we only need one entry in our table,
        # rest are black.
        # Each color is 3 bytes (RGB).
        color_table = bytes(color) + b"\x00" * (3 * 255)

        # Image Descriptor
        image_descriptor = (
            b"\x2C"
            + b"\x00\x00\x00\x00"
            + screen_width
            + screen_height
            + b"\x00"
        )

        # Image Data
        lzw_min_code_size = b"\x08"  # Set to 8 for no compression

        # Image Data Blocks for a single color.
        # Simplest LZW encoding for a single color: clear code, followed
        # by color index, end code.
        image_data_blocks = bytearray(
            [0x02, 0x4C, 0x01, 0x00]
        )  # Compressed data

        # Footer
        footer = b"\x3B"

        # Combine all parts
        return (
            header
            + screen_width
            + screen_height
            + packed_field
            + bg_color_index
            + pixel_aspect_ratio
            + color_table
            + image_descriptor
            + lzw_min_code_size
            + image_data_blocks
            + footer
        )

    def image(
        self,
        image_format: Literal["png", "svg", "bmp", "gif"] = "png",
        width: int = 100,
        height: int = 100,
        color: Tuple[int, int, int] = (0, 0, 255),
    ) -> bytes:
        if image_format not in {"png", "svg", "bmp", "gif"}:
            raise ValueError()
        image_func = getattr(self, image_format)
        return image_func(width=width, height=height, color=color)


class TestFaker(unittest.TestCase):
    def setUp(self) -> None:
        self.faker = Faker()

    def test_first_name(self) -> None:
        first_name: str = self.faker.first_name()
        self.assertIsInstance(first_name, str)
        self.assertTrue(len(first_name) > 0)
        self.assertIn(first_name, self.faker._first_names)

    def test_last_name(self) -> None:
        last_name: str = self.faker.last_name()
        self.assertIsInstance(last_name, str)
        self.assertTrue(len(last_name) > 0)
        self.assertIn(last_name, self.faker._last_names)

    def test_name(self) -> None:
        name: str = self.faker.name()
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)
        parts = name.split(" ")
        first_name = parts[0]
        last_name = " ".join(parts[1:])
        self.assertIn(first_name, self.faker._first_names)
        self.assertIn(last_name, self.faker._last_names)

    def test_word(self) -> None:
        word: str = self.faker.word()
        self.assertIsInstance(word, str)
        self.assertTrue(len(word) > 0)

    def test_words(self) -> None:
        words: List[str] = self.faker.words(nb=3)
        self.assertIsInstance(words, list)
        self.assertEqual(len(words), 3)

    def test_sentence(self) -> None:
        sentence: str = self.faker.sentence()
        self.assertIsInstance(sentence, str)
        self.assertTrue(len(sentence.split()) >= 5)
        self.assertTrue(sentence.endswith("."))

    def test_sentences(self) -> None:
        sentences: List[str] = self.faker.sentences(nb=3)
        self.assertIsInstance(sentences, list)
        self.assertEqual(len(sentences), 3)

    def test_paragraph(self) -> None:
        paragraph: str = self.faker.paragraph()
        self.assertIsInstance(paragraph, str)
        self.assertTrue(len(paragraph.split(".")) >= 5)

    def test_paragraphs(self) -> None:
        paragraphs: List[str] = self.faker.paragraphs(nb=3)
        self.assertIsInstance(paragraphs, list)
        self.assertEqual(len(paragraphs), 3)

    def test_text(self) -> None:
        text: str = self.faker.text(nb_chars=100)
        self.assertIsInstance(text, str)
        self.assertTrue(len(text) <= 100)

    def test_file_name(self) -> None:
        extensions = [(None, "txt"), ("txt", "txt"), ("jpg", "jpg")]
        for extension, expected_extension in extensions:
            with self.subTest(
                extension=extension, expected_extension=expected_extension
            ):
                kwargs = {}
                if extension is not None:
                    kwargs["extension"] = extension
                file_name: str = self.faker.file_name(**kwargs)
                self.assertIsInstance(file_name, str)
                self.assertTrue(file_name.endswith(f".{expected_extension}"))

    def test_email(self) -> None:
        domains = [
            (None, "example.com"),
            ("example.com", "example.com"),
            ("gmail.com", "gmail.com"),
        ]
        for domain, expected_domain in domains:
            with self.subTest(domain=domain, expected_domain=expected_domain):
                kwargs = {}
                if domain is not None:
                    kwargs["domain"] = domain
                email: str = self.faker.email(**kwargs)
                self.assertIsInstance(email, str)
                self.assertTrue(email.endswith(f"@{expected_domain}"))

    def test_url(self) -> None:
        protocols = ("http", "https")
        tlds = ("com", "org", "net", "io")
        suffixes = (".html", ".php", ".go", "", "/")
        for protocol in protocols:
            for tld in tlds:
                for suffix in suffixes:
                    with self.subTest(
                        protocol=protocol, tld=tld, suffix=suffix
                    ):
                        url: str = self.faker.url(
                            protocols=(protocol,),
                            tlds=(tld,),
                            suffixes=(suffix,),
                        )
                        self.assertIsInstance(url, str)
                        self.assertTrue(url.startswith(f"{protocol}://"))
                        self.assertTrue(f".{tld}/" in url)
                        self.assertTrue(
                            url.endswith(suffix) or url.endswith(f"{suffix}/")
                        )

    def test_pyint(self) -> None:
        ranges = [
            (None, None, 0, 9999),
            (0, 5, 0, 5),
            (-5, 0, -5, 0),
        ]
        for min_val, max_val, expected_min_val, expected_max_val in ranges:
            with self.subTest(
                min_value=min_val,
                max_value=max_val,
                expected_min_value=expected_min_val,
                expected_max_value=expected_max_val,
            ):
                kwargs = {}
                if min_val is not None:
                    kwargs["min_value"] = min_val
                if max_val is not None:
                    kwargs["max_value"] = max_val
                val: int = self.faker.pyint(**kwargs)
                self.assertIsInstance(val, int)
                self.assertGreaterEqual(val, expected_min_val)
                self.assertLessEqual(val, expected_max_val)

    def test_pybool(self) -> None:
        value: bool = self.faker.pybool()
        self.assertIsInstance(value, bool)

    def test_pystr(self) -> None:
        ranges = [
            (None, 20),
            (0, 0),
            (1, 1),
            (5, 5),
            (10, 10),
            (100, 100),
        ]
        valid_characters = set(string.ascii_letters)  # ASCII letters

        for nb_chars, expected_nb_chars in ranges:
            with self.subTest(
                nb_chars=nb_chars,
                expected_nb_chars=expected_nb_chars,
            ):
                kwargs = {}
                if nb_chars is not None:
                    kwargs["nb_chars"] = nb_chars
                val: str = self.faker.pystr(**kwargs)

                # Check if the output is a string
                self.assertIsInstance(val, str)

                # Check if the string has the correct length
                self.assertEqual(len(val), expected_nb_chars)

                # Check if all characters are from the valid set
                self.assertTrue(all(c in valid_characters for c in val))

    def test_pyfloat(self) -> None:
        ranges = [
            (None, None, 0.0, 10.0),
            (0.0, 5.0, 0.0, 5.0),
            (-5.0, 0.0, -5.0, 0.0),
        ]
        for min_val, max_val, expected_min_val, expected_max_val in ranges:
            with self.subTest(
                min_value=min_val,
                max_value=max_val,
                expected_min_value=expected_min_val,
                expected_max_value=expected_max_val,
            ):
                kwargs = {}
                if min_val is not None:
                    kwargs["min_value"] = min_val
                if max_val is not None:
                    kwargs["max_value"] = max_val
                val: float = self.faker.pyfloat(**kwargs)
                self.assertIsInstance(val, float)
                self.assertGreaterEqual(val, expected_min_val)
                self.assertLessEqual(val, expected_max_val)

    def test_parse_date_string(self):
        # Test 'now' and 'today' special keywords
        self.assertAlmostEqual(
            self.faker._parse_date_string("now"),
            datetime.now(),
            delta=timedelta(seconds=1),
        )
        self.assertAlmostEqual(
            self.faker._parse_date_string("today"),
            datetime.now(),
            delta=timedelta(seconds=1),
        )

        # Test days, hours, and minutes
        self.assertAlmostEqual(
            self.faker._parse_date_string("1d"),
            datetime.now() + timedelta(days=1),
            delta=timedelta(seconds=1),
        )
        self.assertAlmostEqual(
            self.faker._parse_date_string("-1H"),
            datetime.now() - timedelta(hours=1),
            delta=timedelta(seconds=1),
        )
        self.assertAlmostEqual(
            self.faker._parse_date_string("30M"),
            datetime.now() + timedelta(minutes=30),
            delta=timedelta(seconds=1),
        )

        # Test invalid format
        with self.assertRaises(ValueError):
            self.faker._parse_date_string("1y")

    def test_date_between(self):
        # Test the same date for start and end
        start_date = "now"
        end_date = "+0d"
        random_date = self.faker.date_between(start_date, end_date)
        self.assertIsInstance(random_date, date)
        self.assertEqual(random_date, datetime.now().date())

        # Test date range
        start_date = "-2d"
        end_date = "+2d"
        random_date = self.faker.date_between(start_date, end_date)
        self.assertIsInstance(random_date, date)
        self.assertTrue(
            datetime.now().date() - timedelta(days=2)
            <= random_date
            <= datetime.now().date() + timedelta(days=2)
        )

    def test_date_time_between(self):
        # Test the same datetime for start and end
        start_date = "now"
        end_date = "+0d"
        random_datetime = self.faker.date_time_between(start_date, end_date)
        self.assertIsInstance(random_datetime, datetime)
        self.assertAlmostEqual(
            random_datetime, datetime.now(), delta=timedelta(seconds=1)
        )

        # Test datetime range
        start_date = "-2H"
        end_date = "+2H"
        random_datetime = self.faker.date_time_between(start_date, end_date)
        self.assertIsInstance(random_datetime, datetime)
        self.assertTrue(
            datetime.now() - timedelta(hours=2)
            <= random_datetime
            <= datetime.now() + timedelta(hours=2)
        )

    def test_text_pdf(self):
        pdf = self.faker.pdf(generator=TextPdfGenerator)
        self.assertTrue(pdf)

    def test_graphic_pdf(self):
        pdf = self.faker.pdf(generator=GraphicPdfGenerator)
        self.assertTrue(pdf)

    def test_png(self):
        png = self.faker.png()
        self.assertTrue(png)

    def test_svg(self):
        svg = self.faker.svg()
        self.assertTrue(svg)

    def test_bmp(self):
        bmp = self.faker.bmp()
        self.assertTrue(bmp)

    def test_gif(self):
        gif = self.faker.gif()
        self.assertTrue(gif)


if __name__ == "__main__":
    unittest.main()
