"""
https://github.com/barseghyanartur/fake.py/
"""

import asyncio
import contextlib
import io
import logging
import os
import random
import re
import string
import unittest
import uuid
import zipfile
import zlib
from abc import abstractmethod
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from tempfile import NamedTemporaryFile, gettempdir
from threading import Lock
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Set,
    TextIO,
    Tuple,
    Type,
    Union,
)

__title__ = "fake.py"
__version__ = "0.3"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "AuthorshipData",
    "BaseStorage",
    "DjangoModelFactory",
    "DocxGenerator",
    "FACTORY",
    "FAKER",
    "FILE_REGISTRY",
    "Factory",
    "Faker",
    "FileRegistry",
    "FileSystemStorage",
    "GraphicPdfGenerator",
    "MetaData",
    "ModelFactory",
    "StringValue",
    "SubFactory",
    "TextPdfGenerator",
    "TortoiseModelFactory",
    "post_save",
    "pre_save",
)

LOGGER = logging.getLogger(__name__)

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

DOCX_TPL_DOC_HEADER = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'  # noqa
    "<w:body>"
)

DOCX_TPL_DOC_FOOTER = "</w:body></w:document>"

DOC_TPL_DOC_STRUCTURE_RELS = (
    b"<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
    b"<Relationships xmlns='http://schemas.openxmlformats.org/package/2006/relationships'>"  # noqa
    b"<Relationship Id='rId1' Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument' Target='word/document.xml'/>"  # noqa
    b"</Relationships>"
)

DOC_TPL_DOC_STRUCTURE_WORD_RELS = (
    b"<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
    b"<Relationships xmlns='http://schemas.openxmlformats.org/package/2006/relationships'>"  # noqa
    b"<Relationship Id='rId1' Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles' Target='styles.xml'/>"  # noqa
    b"</Relationships>"
)

DOC_TPL_DOC_STRUCTURE_WORD_STYLES = (
    b"<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
    b"<w:styles xmlns:w='http://schemas.openxmlformats.org/wordprocessingml/2006/main'>"  # noqa
    b"<w:style w:type='paragraph' w:default='1' w:styleId='Normal'>"
    b"<w:name w:val='Normal'/><w:qFormat/></w:style></w:styles>"
)

DOC_TPL_DOC_STRUCTURE_CONTENT_TYPES = (
    b"<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
    b"<Types xmlns='http://schemas.openxmlformats.org/package/2006/content-types'>"  # noqa
    b"<Default Extension='rels' ContentType='application/vnd.openxmlformats-package.relationships+xml'/>"  # noqa
    b"<Default Extension='xml' ContentType='application/xml'/>"
    b"<Override PartName='/word/document.xml' ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'/>"  # noqa
    b"<Override PartName='/word/styles.xml' ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml'/>"  # noqa
    b"</Types>"
)


class MetaData:
    __slots__ = ("content",)

    def __init__(self):
        self.content: Optional[str] = None

    def add_content(self, content: Union[str, List[str]]) -> None:
        if isinstance(content, list):
            self.content = "\n".join(content)
        else:
            self.content = content


class StringValue(str):
    __slots__ = ("data",)

    data: Dict[str, Any]

    def __new__(cls, value, *args, **kwargs):
        obj = str.__new__(cls, value)
        obj.data = {}
        return obj


class FileRegistry:
    """Stores list `StringValue` instances.

    .. code-block:: python

        from fake import FAKER, FILE_REGISTRY

        txt_file_1 = FAKER.txt_file()
        txt_file_2 = FAKER.txt_file()
        ...
        txt_file_n = FAKER.txt_file()

        # The FileRegistry._registry would then contain this:
        {
            txt_file_1,
            txt_file_2,
            ...,
            txt_file_n,
        }

        # Clean up created files as follows:
        FILE_REGISTRY.clean_up()
    """

    def __init__(self):
        self._registry: Set[StringValue] = set()
        self._lock = Lock()

    def add(self, string_value: StringValue) -> None:
        with self._lock:
            self._registry.add(string_value)

    def remove(self, string_value: Union[StringValue, str]) -> bool:
        if not isinstance(string_value, StringValue):
            string_value = self.search(string_value)

        if not string_value:
            return False

        with self._lock:
            # No error if the element doesn't exist
            self._registry.discard(string_value)
            try:
                string_value.data["storage"].unlink(
                    string_value.data["filename"]
                )
                return True
            except Exception as e:
                LOGGER.error(
                    f"Failed to unlink file "
                    f"{string_value.data['filename']}: {e}"
                )
            return False

    def search(self, value: str) -> Optional[StringValue]:
        with self._lock:
            for string_value in self._registry:
                if string_value == value:
                    return string_value
        return None

    def clean_up(self) -> None:
        with self._lock:
            while self._registry:
                file = self._registry.pop()
                try:
                    file.data["storage"].unlink(file.data["filename"])
                except Exception as err:
                    LOGGER.error(
                        f"Failed to unlink file {file.data['filename']}: {err}"
                    )


FILE_REGISTRY = FileRegistry()


class BaseStorage:
    """Base storage."""

    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    @abstractmethod
    def generate_filename(
        self: "BaseStorage",
        extension: str,
        prefix: Optional[str] = None,
        basename: Optional[str] = None,
    ) -> Any:
        """Generate filename."""

    @abstractmethod
    def write_text(
        self: "BaseStorage",
        filename: Any,
        data: str,
        encoding: Optional[str] = None,
    ) -> int:
        """Write text."""

    @abstractmethod
    def write_bytes(self: "BaseStorage", filename: Any, data: bytes) -> int:
        """Write bytes."""

    @abstractmethod
    def exists(self: "BaseStorage", filename: Any) -> bool:
        """Check if file exists."""

    @abstractmethod
    def relpath(self: "BaseStorage", filename: Any) -> str:
        """Return relative path."""

    @abstractmethod
    def abspath(self: "BaseStorage", filename: Any) -> str:
        """Return absolute path."""

    @abstractmethod
    def unlink(self: "BaseStorage", filename: Any) -> None:
        """Delete the file."""


class FileSystemStorage(BaseStorage):
    """File storage class using pathlib for path handling.

    Usage example:

    .. code-block:: python

        from fake import Faker, FileSystemStorage

        FAKER = Faker()

        storage = FileSystemStorage()
        docx_file = storage.generate_filename(prefix="zzz_", extension="docx")
        storage.write_bytes(docx_file, FAKER.docx())

    Initialization with params:

    .. code-block:: python

        from fake import Faker, FileSystemStorage

        FAKER = Faker()

        storage = FileSystemStorage()
        docx_file = FAKER.docx_file(storage=storage)
    """

    def __init__(
        self: "FileSystemStorage",
        root_path: Optional[str] = gettempdir(),
        rel_path: Optional[str] = "tmp",
        *args,
        **kwargs,
    ) -> None:
        """
        :param root_path: Path of your files root directory (e.g., Django's
            `settings.MEDIA_ROOT`).
        :param rel_path: Relative path (from root directory).
        """
        self.root_path = Path(root_path or "")
        self.rel_path = Path(rel_path or "")
        super().__init__(*args, **kwargs)

    def generate_filename(
        self: "FileSystemStorage",
        extension: str,
        prefix: Optional[str] = None,
        basename: Optional[str] = None,
    ) -> str:
        """Generate filename."""
        dir_path = self.root_path / self.rel_path
        dir_path.mkdir(parents=True, exist_ok=True)

        if not extension:
            raise Exception("Extension shall be given!")

        if basename:
            return str(dir_path / f"{basename}.{extension}")
        else:
            temp_file = NamedTemporaryFile(
                prefix=prefix,
                dir=str(dir_path),
                suffix=f".{extension}",
                delete=False,
            )
            return temp_file.name

    def write_text(
        self: "FileSystemStorage",
        filename: str,
        data: str,
        encoding: Optional[str] = None,
    ) -> int:
        """Write text."""
        path = Path(filename)
        path.write_text(data, encoding=encoding or "utf-8")
        return len(data)

    def write_bytes(
        self: "FileSystemStorage",
        filename: str,
        data: bytes,
    ) -> int:
        """Write bytes."""
        path = Path(filename)
        path.write_bytes(data)
        return len(data)

    def exists(self: "FileSystemStorage", filename: str) -> bool:
        """Check if file exists."""
        file_path = Path(filename)
        if file_path.is_absolute():
            return file_path.exists()
        return (self.root_path / file_path).exists()

    def relpath(self: "FileSystemStorage", filename: str) -> str:
        """Return relative path."""
        return str(Path(filename).relative_to(self.root_path))

    def abspath(self: "FileSystemStorage", filename: str) -> str:
        """Return absolute path."""
        file_path = Path(filename)
        if file_path.is_absolute():
            return str(file_path.resolve())
        return str((self.root_path / file_path).resolve())

    def unlink(self: "FileSystemStorage", filename: str) -> None:
        """Delete the file."""
        file_path = Path(filename)
        if file_path.is_absolute():
            file_path.unlink()
        else:
            (self.root_path / file_path).unlink()


class TextPdfGenerator:
    """Text PDF generatr.

    Usage example:

    .. code-block:: python

        from pathlib import Path
        from fake import Faker, TextPdfGenerator

        FAKER = Faker()

        Path("/tmp/text_example.pdf").write_bytes(
            FAKER.pdf(nb_pages=100, generator=TextPdfGenerator)
        )
    """

    nb_pages: int
    texts: List[str]

    def __init__(self, faker: "Faker") -> None:
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
        metadata: Optional[MetaData] = None,
        **kwargs,
    ) -> bytes:
        # Initialization
        if not nb_pages and not texts:
            raise ValueError(
                "Either `nb_pages` or `texts` arguments shall be given."
            )
        if texts:
            self.nb_pages: int = len(texts)
            self.texts = texts
        else:
            self.nb_pages: int = nb_pages or 1
            self.texts = self.faker.sentences(nb=self.nb_pages)

        if metadata:
            metadata.add_content(self.texts)

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
        from fake import Faker, GraphicPdfGenerator

        FAKER = Faker()

        Path("/tmp/graphic_example.pdf").write_bytes(
            FAKER.pdf(nb_pages=100, generator=GraphicPdfGenerator)
        )
    """

    nb_pages: int
    image_size: Tuple[int, int]
    image_color: Tuple[int, int, int]

    def __init__(self, faker: "Faker") -> None:
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
        **kwargs,
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

    def _extract_info(self, file: TextIO) -> List[str]:
        return [
            line.strip()
            for line in file
            if "__author__" in line or "Author:" in line
        ]

    def _find_authorship_info(self, file_path: str) -> List[str]:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return self._extract_info(file)
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as file:
                return self._extract_info(file)

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


class DocxGenerator:
    """DocxGenerator - generates a DOCX file with text.

    Usage example:

    .. code-block:: python

        from pathlib import Path
        from fake import Faker

        FAKER = Faker()
        Path("/tmp/example.docx").write_bytes(FAKER.docx(nb_pages=100))
    """

    def __init__(self, faker: "Faker") -> None:
        self.faker = faker

    def _create_page(self, text: str, is_last_page: bool) -> str:
        page_content = f"<w:p><w:r><w:t>{text}</w:t></w:r></w:p>"
        if not is_last_page:
            page_content += '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
        return page_content

    def create(
        self,
        nb_pages: Optional[int] = None,
        texts: Optional[List[str]] = None,
        metadata: Optional[MetaData] = None,
    ) -> bytes:
        if not nb_pages and not texts:
            raise ValueError(
                "Either `nb_pages` or `texts` arguments shall be given."
            )
        if texts:
            nb_pages = len(texts)
        else:
            texts = self.faker.sentences(nb=nb_pages)  # type: ignore

        if metadata:
            metadata.add_content(texts)

        # Construct the main document content
        document_content = DOCX_TPL_DOC_HEADER
        for i, page_text in enumerate(texts):
            document_content += self._create_page(
                page_text, i == nb_pages - 1  # type: ignore
            )
        document_content += DOCX_TPL_DOC_FOOTER

        # Basic structure of a DOCX file
        docx_structure = {
            "word/document.xml": document_content.encode(),
            "_rels/.rels": DOC_TPL_DOC_STRUCTURE_RELS,
            "word/_rels/document.xml.rels": DOC_TPL_DOC_STRUCTURE_WORD_RELS,
            "word/styles.xml": DOC_TPL_DOC_STRUCTURE_WORD_STYLES,
            "[Content_Types].xml": DOC_TPL_DOC_STRUCTURE_CONTENT_TYPES,
        }

        # Create the DOCX file (ZIP archive)
        docx_bytes = io.BytesIO()
        with zipfile.ZipFile(docx_bytes, "w") as docx:
            for path, content in docx_structure.items():
                docx.writestr(path, content)

        return docx_bytes.getvalue()


class Faker:
    """fake.py - simplified, standalone alternative with no dependencies.

    ----

    Usage example:

    .. code-block:: python

        from fake import Faker

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
        from fake import Faker, TextPdfGenerator, GraphicPdfGenerator

        FAKER = Faker()

        Path("/tmp/graphic_pdf.pdf").write_bytes(
            FAKER.pdf(nb_pages=100, generator=GraphicPdfGenerator)
        )

        Path("/tmp/text_pdf.pdf").write_bytes(
            FAKER.pdf(nb_pages=100, generator=TextPdfGenerator)
        )

    ----

    Various image formats:

    .. code-block:: python

        from pathlib import Path
        from fake import Faker

        FAKER = Faker()

        Path("/tmp/image.png").write_bytes(FAKER.png())

        Path("/tmp/image.svg").write_bytes(FAKER.svg())

        Path("/tmp/image.bmp").write_bytes(FAKER.bmp())

        Path("/tmp/image.gif").write_bytes(FAKER.gif())

    Note, that all image formats accept `size` (default: `(100, 100)`)
    and `color`(default: `(255, 0, 0)`) arguments.
    """

    def __init__(self) -> None:
        self._words: List[str] = []
        self._first_names: List[str] = []
        self._last_names: List[str] = []

        self.load_words()
        self.load_names()

    def load_words(self) -> None:
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

    def load_names(self) -> None:
        authorship_data = AuthorshipData()
        self._first_names = list(authorship_data.first_names)
        self._last_names = list(authorship_data.last_names)

    @staticmethod
    def _rot13_translate(text: str, translation_map: Dict[str, str]) -> str:
        return "".join([translation_map.get(c, c) for c in text])

    def uuid(self) -> uuid.UUID:
        return uuid.uuid4()

    def first_name(self) -> str:
        return random.choice(self._first_names)

    def last_name(self) -> str:
        return random.choice(self._last_names)

    def name(self) -> str:
        return f"{self.first_name()} {self.last_name()}"

    def username(self) -> str:
        return (
            f"{self.word()}_{self.word()}_{self.word()}_{self.pystr()}"
        ).lower()

    def slug(self) -> str:
        return (
            f"{self.word()}-{self.word()}-{self.word()}-{self.pystr()}"
        ).lower()

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

    def texts(self, nb: int = 3) -> List[str]:
        return [self.text() for _ in range(nb)]

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

    def date(
        self,
        start_date: str = "-7d",
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

    def date_time(
        self,
        start_date: str = "-7d",
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
        metadata: Optional[MetaData] = None,
        **kwargs,
    ) -> bytes:
        """Create a PDF document of a given size."""
        _pdf = generator(faker=self)
        return _pdf.create(nb_pages=nb_pages, metadata=metadata, **kwargs)

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
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
    ) -> bytes:
        if image_format not in {"png", "svg", "bmp", "gif"}:
            raise ValueError()
        image_func = getattr(self, image_format)
        return image_func(size=size, color=color)

    def docx(
        self,
        nb_pages: Optional[int] = 1,
        texts: Optional[List[str]] = None,
        metadata: Optional[MetaData] = None,
    ) -> bytes:
        _docx = DocxGenerator(faker=self)
        return _docx.create(nb_pages=nb_pages, texts=texts, metadata=metadata)

    def pdf_file(
        self,
        nb_pages: int = 1,
        generator: Union[
            Type[TextPdfGenerator], Type[GraphicPdfGenerator]
        ] = GraphicPdfGenerator,
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
        **kwargs,
    ) -> StringValue:
        if storage is None:
            storage = FileSystemStorage()
        filename = storage.generate_filename(
            extension="pdf",
            prefix=prefix,
            basename=basename,
        )
        metadata = MetaData()
        data = self.pdf(
            nb_pages=nb_pages, generator=generator, metadata=metadata, **kwargs
        )
        storage.write_bytes(filename=filename, data=data)
        file = StringValue(storage.relpath(filename))
        file.data = {
            "storage": storage,
            "filename": filename,
            "content": metadata.content,
        }
        FILE_REGISTRY.add(file)
        return file

    def _image_file(
        self,
        extension: str,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
    ) -> StringValue:
        if storage is None:
            storage = FileSystemStorage()
        filename = storage.generate_filename(
            extension=extension,
            prefix=prefix,
            basename=basename,
        )
        data = self.png(size=size, color=color)
        storage.write_bytes(filename=filename, data=data)
        file = StringValue(storage.relpath(filename))
        file.data = {"storage": storage, "filename": filename}
        FILE_REGISTRY.add(file)
        return file

    def png_file(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
    ) -> StringValue:
        return self._image_file(
            extension="png",
            size=size,
            color=color,
            storage=storage,
            basename=basename,
            prefix=prefix,
        )

    def svg_file(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
    ) -> StringValue:
        return self._image_file(
            extension="svg",
            size=size,
            color=color,
            storage=storage,
            basename=basename,
            prefix=prefix,
        )

    def bmp_file(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
    ) -> StringValue:
        return self._image_file(
            extension="bmp",
            size=size,
            color=color,
            storage=storage,
            basename=basename,
            prefix=prefix,
        )

    def gif_file(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
    ) -> StringValue:
        return self._image_file(
            extension="gif",
            size=size,
            color=color,
            storage=storage,
            basename=basename,
            prefix=prefix,
        )

    def docx_file(
        self,
        nb_pages: int = 1,
        texts: Optional[List[str]] = None,
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
    ) -> StringValue:
        if storage is None:
            storage = FileSystemStorage()
        filename = storage.generate_filename(
            extension="docx",
            prefix=prefix,
            basename=basename,
        )
        metadata = MetaData()
        data = self.docx(texts=texts, metadata=metadata)
        storage.write_bytes(filename=filename, data=data)
        file = StringValue(storage.relpath(filename))
        file.data = {
            "storage": storage,
            "filename": filename,
            "content": metadata.content,
        }
        FILE_REGISTRY.add(file)
        return file

    def txt_file(
        self,
        nb_chars: Optional[int] = 200,
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
        text: Optional[str] = None,
    ) -> StringValue:
        if storage is None:
            storage = FileSystemStorage()
        filename = storage.generate_filename(
            extension="txt",
            prefix=prefix,
            basename=basename,
        )
        if not text:
            if not nb_chars:
                nb_chars = 200
            text = self.text(nb_chars=nb_chars)
        storage.write_text(filename=filename, data=text)
        file = StringValue(storage.relpath(filename))
        file.data = {
            "storage": storage,
            "filename": filename,
            "content": text,
        }
        FILE_REGISTRY.add(file)
        return file


FAKER = Faker()


class FactoryMethod:
    def __init__(
        self,
        method_name: str,
        faker: Optional[Faker] = None,
        **kwargs,
    ):
        self.method_name = method_name
        self.kwargs = kwargs
        self.faker = faker or FAKER

    def __call__(self):
        method = getattr(self.faker, self.method_name)
        return method(**self.kwargs)


class FactoryMeta(type):
    # List of methods to be created in the Factory class
    enabled_methods = {
        "bmp_file",
        "date",
        "date_time",
        "docx_file",
        "email",
        "first_name",
        "ipv4",
        "last_name",
        "name",
        "paragraph",
        "pdf_file",
        "png_file",
        "pybool",
        "pyfloat",
        "pyint",
        "pystr",
        "sentence",
        "slug",
        "svg_file",
        "text",
        "txt_file",
        "txt_file",
        "url",
        "username",
        "uuid",
        "word",
    }

    def __new__(cls, name, bases, attrs):
        for method_name in cls.enabled_methods:
            attrs[method_name] = cls.create_factory_method(method_name)
        return super().__new__(cls, name, bases, attrs)

    @staticmethod
    def create_factory_method(method_name):
        def method(self, **kwargs):
            # # Special handling for boolean
            # if method_name == "pybool":
            #     return FactoryMethod("pybool")
            # # Default argument for text
            # if method_name == "text" and "nb_chars" not in kwargs:
            #     kwargs["max_nb_chars"] = 200
            return FactoryMethod(method_name, faker=self.faker, **kwargs)

        # return staticmethod(method)
        return method


class SubFactory:
    def __init__(self, factory_class, **kwargs):
        self.factory_class = factory_class
        self.factory_kwargs = kwargs

    def __call__(self):
        # Initialize the specified factory class and create an instance
        return self.factory_class.create(**self.factory_kwargs)


class Factory(metaclass=FactoryMeta):
    """Factory."""

    def __init__(self, faker: Optional[Faker] = None) -> None:
        self.faker = faker or FAKER


FACTORY = Factory(faker=FAKER)


def pre_save(func):
    func.is_pre_save = True
    return func


def post_save(func):
    func.is_post_save = True
    return func


class ModelFactory:
    """ModelFactory."""

    class Meta:
        get_or_create = ("id",)  # Default fields for get_or_create

    def __init_subclass__(cls, **kwargs):
        base_meta = getattr(
            cls.__bases__[0],
            "_meta",
            {
                attr: getattr(cls.__bases__[0].Meta, attr)
                for attr in dir(cls.__bases__[0].Meta)
                if not attr.startswith("_")
            },
        )
        cls_meta = {
            attr: getattr(cls.Meta, attr)
            for attr in dir(cls.Meta)
            if not attr.startswith("_")
        }

        cls._meta = {**base_meta, **cls_meta}

    @classmethod
    def _run_hooks(cls, hooks, instance):
        for method in hooks:
            getattr(cls, method)(instance)

    @classmethod
    def create(cls, **kwargs):
        model_data = {
            field: (
                value()
                if isinstance(value, (FactoryMethod, SubFactory))
                else value
            )
            for field, value in cls.__dict__.items()
            if not field.startswith("_") and not field == "Meta"
        }
        model_data.update(kwargs)

        instance = cls.Meta.model(**model_data)

        pre_save_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_pre_save", False)
        ]
        cls._run_hooks(pre_save_hooks, instance)

        cls.save(instance)

        post_save_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_post_save", False)
        ]
        cls._run_hooks(post_save_hooks, instance)

        return instance

    @classmethod
    def create_batch(cls, count, **kwargs):
        return [cls.create(**kwargs) for _ in range(count)]

    def __new__(cls, **kwargs):
        return cls.create(**kwargs)

    @classmethod
    def save(cls, instance):
        """Save the instance."""


class DjangoModelFactory(ModelFactory):
    """Django ModelFactory."""

    @classmethod
    def save(cls, instance):
        instance.save()

    @classmethod
    def create(cls, **kwargs):
        model = cls.Meta.model
        unique_fields = cls._meta.get("get_or_create", ["id"])

        # Construct a query for unique fields
        query = {
            field: kwargs[field] for field in unique_fields if field in kwargs
        }

        # Try to get an existing instance
        if query:
            instance = model.objects.filter(**query).first()
            if instance:
                return instance

        # Create a new instance if none found
        # return super().create(**kwargs)
        model_data = {
            field: value
            for field, value in cls.__dict__.items()
            if not field.startswith("_") and not field == "Meta"
        }

        # Separate nested attributes and direct attributes
        nested_attrs = {k: v for k, v in kwargs.items() if "__" in k}
        direct_attrs = {k: v for k, v in kwargs.items() if "__" not in k}

        # Update direct attributes with callable results
        for field, value in model_data.items():
            if isinstance(value, (FactoryMethod, SubFactory)):
                model_data[field] = (
                    value()
                    if field not in direct_attrs
                    else direct_attrs[field]
                )

        # Create instance
        instance = cls.Meta.model(**model_data)

        # Handle nested attributes
        for attr, value in nested_attrs.items():
            field_name, nested_attr = attr.split("__", 1)
            if isinstance(getattr(cls, field_name, None), SubFactory):
                related_instance = getattr(
                    cls, field_name
                ).factory_class.create(**{nested_attr: value})
                setattr(instance, field_name, related_instance)

        # Run pre-save hooks
        pre_save_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_pre_save", False)
        ]
        cls._run_hooks(pre_save_hooks, instance)

        # Save instance
        cls.save(instance)

        # Run post-save hooks
        post_save_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_post_save", False)
        ]
        cls._run_hooks(post_save_hooks, instance)

        return instance


class TortoiseModelFactory(ModelFactory):
    """Tortoise ModelFactory."""

    @classmethod
    def save(cls, instance):
        async def async_save():
            await instance.save()

        asyncio.run(async_save())

    @classmethod
    def create(cls, **kwargs):
        model = cls.Meta.model
        unique_fields = cls._meta.get("get_or_create", ["id"])

        # Construct a query for unique fields
        query = {
            field: kwargs[field] for field in unique_fields if field in kwargs
        }

        # Try to get an existing instance
        if query:

            async def async_filter():
                return await model.filter(**query).first()

            instance = asyncio.run(async_filter())

            if instance:
                return instance

        # Create a new instance if none found
        return super().create(**kwargs)


# TODO: Remove once Python 3.8 support is dropped
class ClassProperty(property):
    """ClassProperty."""

    def __get__(self, cls, owner):
        """Get."""
        return classmethod(self.fget).__get__(None, owner)()


classproperty = ClassProperty


class TestFaker(unittest.TestCase):
    def setUp(self) -> None:
        self.faker = FAKER

    def tearDown(self):
        FILE_REGISTRY.clean_up()

    def test_uuid(self) -> None:
        uuid_value = self.faker.uuid()
        self.assertIsInstance(uuid_value, uuid.UUID)

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

    def test_texts(self) -> None:
        texts: List[str] = self.faker.texts(nb=3)
        self.assertIsInstance(texts, list)
        self.assertEqual(len(texts), 3)

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
                kwargs = {"domain": domain}
                email: str = self.faker.email(**kwargs)  # type: ignore
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

    def test_ipv4(self) -> None:
        # Test a large number of IPs to ensure randomness and correctness
        for _ in range(1000):
            ip = self.faker.ipv4()
            self.assertIsNotNone(ip)
            self.assertIsInstance(ip, str)

            parts = ip.split(".")
            self.assertEqual(len(parts), 4)

            for part in parts:
                self.assertTrue(part.isdigit())
                self.assertTrue(0 <= int(part) <= 255)

    def test_parse_date_string(self) -> None:
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

    def test_date(self) -> None:
        # Test the same date for start and end
        start_date = "now"
        end_date = "+0d"
        random_date = self.faker.date(start_date, end_date)
        self.assertIsInstance(random_date, date)
        self.assertEqual(random_date, datetime.now().date())

        # Test date range
        start_date = "-2d"
        end_date = "+2d"
        random_date = self.faker.date(start_date, end_date)
        self.assertIsInstance(random_date, date)
        self.assertTrue(
            datetime.now().date() - timedelta(days=2)
            <= random_date
            <= datetime.now().date() + timedelta(days=2)
        )

    def test_date_time(self) -> None:
        # Test the same datetime for start and end
        start_date = "now"
        end_date = "+0d"
        random_datetime = self.faker.date_time(start_date, end_date)
        self.assertIsInstance(random_datetime, datetime)
        self.assertAlmostEqual(
            random_datetime, datetime.now(), delta=timedelta(seconds=1)
        )

        # Test datetime range
        start_date = "-2H"
        end_date = "+2H"
        random_datetime = self.faker.date_time(start_date, end_date)
        self.assertIsInstance(random_datetime, datetime)
        self.assertTrue(
            datetime.now() - timedelta(hours=2)
            <= random_datetime
            <= datetime.now() + timedelta(hours=2)
        )

    def test_text_pdf(self) -> None:
        with self.subTest("All params None, should fail"):
            with self.assertRaises(ValueError):
                self.faker.pdf(
                    nb_pages=None,  # type: ignore
                    texts=None,
                    generator=TextPdfGenerator,
                )

        with self.subTest("Without params"):
            pdf = self.faker.pdf(generator=TextPdfGenerator)
            self.assertTrue(pdf)
            self.assertIsInstance(pdf, bytes)

        with self.subTest("With `texts` provided"):
            texts = self.faker.sentences()
            pdf = self.faker.pdf(texts=texts, generator=TextPdfGenerator)
            self.assertTrue(pdf)
            self.assertIsInstance(pdf, bytes)

    def test_graphic_pdf(self) -> None:
        pdf = self.faker.pdf(generator=GraphicPdfGenerator)
        self.assertTrue(pdf)
        self.assertIsInstance(pdf, bytes)

    def test_png(self) -> None:
        png = self.faker.png()
        self.assertTrue(png)
        self.assertIsInstance(png, bytes)

    def test_svg(self) -> None:
        svg = self.faker.svg()
        self.assertTrue(svg)
        self.assertIsInstance(svg, bytes)

    def test_bmp(self) -> None:
        bmp = self.faker.bmp()
        self.assertTrue(bmp)
        self.assertIsInstance(bmp, bytes)

    def test_gif(self) -> None:
        gif = self.faker.gif()
        self.assertTrue(gif)
        self.assertIsInstance(gif, bytes)

    def test_image(self):
        for image_format in {"png", "svg", "bmp", "gif"}:
            with self.subTest(image_format=image_format):
                image = self.faker.image(
                    image_format=image_format,  # type: ignore
                )
                self.assertTrue(image)
                self.assertIsInstance(image, bytes)
        for image_format in {"bin"}:
            with self.subTest(image_format=image_format):
                with self.assertRaises(ValueError):
                    self.faker.image(image_format=image_format)  # type: ignore

    def test_docx(self) -> None:
        with self.subTest("All params None, should fail"):
            with self.assertRaises(ValueError):
                self.faker.docx(nb_pages=None, texts=None),  # noqa

        with self.subTest("Without params"):
            docx = self.faker.docx()
            self.assertTrue(docx)
            self.assertIsInstance(docx, bytes)

        with self.subTest("With `texts` provided"):
            texts = self.faker.sentences()
            docx = self.faker.docx(texts=texts)
            self.assertTrue(docx)
            self.assertIsInstance(docx, bytes)

    def test_pdf_file(self) -> None:
        file = self.faker.pdf_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_png_file(self) -> None:
        file = self.faker.png_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_svg_file(self) -> None:
        file = self.faker.svg_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_bmp_file(self) -> None:
        file = self.faker.bmp_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_gif_file(self) -> None:
        file = self.faker.gif_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_docx_file(self) -> None:
        file = self.faker.docx_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_txt_file(self) -> None:
        file = self.faker.txt_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_storage(self) -> None:
        storage = FileSystemStorage()
        with self.assertRaises(Exception):
            storage.generate_filename(extension=None)

    def test_storage_integration(self) -> None:
        file = self.faker.txt_file()
        file_2 = self.faker.txt_file(basename="file_2")
        file_3 = self.faker.txt_file(basename="file_3")
        storage: FileSystemStorage = file.data["storage"]

        with self.subTest("Test os.path.exists"):
            self.assertTrue(os.path.exists(file.data["filename"]))

        with self.subTest("Test storage.exists on StringValue"):
            self.assertTrue(storage.exists(file))
        with self.subTest("Test storage.exists on rel path"):
            self.assertTrue(storage.exists(str(file)))
        with self.subTest("Test storage.exists on abs path"):
            self.assertTrue(storage.exists(file.data["filename"]))

        with self.subTest("Test storage.abspath"):
            self.assertEqual(storage.abspath(str(file)), file.data["filename"])

        with self.subTest("Test storage.unlink on absolute path"):
            storage.unlink(file.data["filename"])
        self.assertFalse(storage.exists(str(file)))
        self.assertFalse(storage.exists(file.data["filename"]))

        with self.subTest("Test storage.unlink on relative path"):
            storage.unlink(str(file_2))
            self.assertFalse(storage.exists(file_2.data["filename"]))

        with self.subTest("Test storage.unlink on relative path"):
            storage.unlink(str(file_3))
            self.assertFalse(storage.exists(file_3.data["filename"]))

    def test_metadata(self) -> None:
        """Test MetaData."""
        with self.subTest("Test str"):
            metadata = MetaData()
            content = FAKER.word()
            metadata.add_content(content)
            self.assertEqual(metadata.content, content)
        with self.subTest("Test list"):
            metadata = MetaData()
            content = FAKER.words()
            metadata.add_content(content)
            self.assertEqual(metadata.content, "\n".join(content))

    def test_factory_method(self) -> None:
        """Test FactoryMethod."""
        with self.subTest("sentence"):
            sentence_factory_method = FactoryMethod("sentence")
            generated_sentence = sentence_factory_method()
            self.assertIsInstance(generated_sentence, str)
        with self.subTest("pyint"):
            pyint_factory_method = FactoryMethod("pyint")
            generated_int = pyint_factory_method()
            self.assertIsInstance(generated_int, int)

    def test_factory_meta(self) -> None:
        class TestFactory(Factory):
            pass

        for method_name in FactoryMeta.enabled_methods:
            self.assertTrue(hasattr(TestFactory, method_name))

    def test_sub_factory(self) -> None:
        """Test FACTORY and SubFactory."""
        # *************************
        # ********* Models ********
        # *************************

        class QuerySet(list):
            """Mimicking Django QuerySet class."""

            def __init__(self, instance: Union["Article", "User"]) -> None:
                super().__init__()
                self.instance = instance

            def first(self) -> Union["Article", "User"]:
                return self.instance

        class Manager:
            """Mimicking Django Manager class."""

            def __init__(self, instance: Union["Article", "User"]) -> None:
                self.instance = instance

            def filter(self, *args, **kwargs) -> "QuerySet":
                return QuerySet(instance=self.instance)

        @dataclass
        class User:
            """User model."""

            id: int
            username: str
            first_name: str
            last_name: str
            email: str
            last_login: Optional[datetime]
            date_joined: Optional[datetime]
            password: Optional[str] = None
            is_superuser: bool = False
            is_staff: bool = False
            is_active: bool = True

            def save(self, *args, **kwargs):
                """Mimicking Django's Mode save method."""
                self.save_called = True

            # TODO: Remove once Python 3.8 support is dropped
            #  and replace with @classmethod @property combo.
            @classproperty
            def objects(cls):
                """Mimicking Django's Manager behaviour."""
                return Manager(
                    instance=cls(
                        id=FAKER.pyint(),
                        username=FAKER.username(),
                        first_name=FAKER.first_name(),
                        last_name=FAKER.last_name(),
                        email=FAKER.email(),
                        last_login=FAKER.date_time(),
                        date_joined=FAKER.date_time(),
                    )
                )

        @dataclass
        class Article:
            id: int
            title: str
            slug: str
            content: str
            author: User
            image: Optional[
                str
            ] = None  # Use str to represent the image path or URL
            pub_date: datetime = datetime.now()
            safe_for_work: bool = False
            minutes_to_read: int = 5

            def save(self, *args, **kwargs):
                """Mimicking Django's Mode save method."""
                self.save_called = True

            # TODO: Remove once Python 3.8 support is dropped
            #  and replace with @classmethod @property combo.
            @classproperty
            def objects(cls):
                """Mimicking Django's Manager behaviour."""
                return Manager(
                    instance=cls(
                        id=FAKER.pyint(),
                        title=FAKER.word(),
                        slug=FAKER.slug(),
                        content=FAKER.text(),
                        author=User(
                            id=FAKER.pyint(),
                            username=FAKER.username(),
                            first_name=FAKER.first_name(),
                            last_name=FAKER.last_name(),
                            email=FAKER.email(),
                            last_login=FAKER.date_time(),
                            date_joined=FAKER.date_time(),
                        ),
                    )
                )

        # ****************************
        # *********** Other **********
        # ****************************

        BASE_DIR = Path(__file__).resolve().parent.parent
        MEDIA_ROOT = BASE_DIR / "media"

        STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")

        # ****************************
        # ******* ModelFactory *******
        # ****************************

        class UserFactory(ModelFactory):
            id = FACTORY.pyint()
            username = FACTORY.username()
            first_name = FACTORY.first_name()
            last_name = FACTORY.last_name()
            email = FACTORY.email()
            last_login = FACTORY.date_time()
            is_superuser = False
            is_staff = False
            is_active = FACTORY.pybool()
            date_joined = FACTORY.date_time()

            class Meta:
                model = User

            @staticmethod
            @pre_save
            def __pre_save_method(instance):
                instance.pre_save_called = True

            @staticmethod
            @post_save
            def __post_save_method(instance):
                instance.post_save_called = True

        class ArticleFactory(ModelFactory):
            id = FACTORY.pyint()
            title = FACTORY.sentence()
            slug = FACTORY.slug()
            content = FACTORY.text()
            image = FACTORY.png_file(storage=STORAGE)
            pub_date = FACTORY.date()
            safe_for_work = FACTORY.pybool()
            minutes_to_read = FACTORY.pyint(min_value=1, max_value=10)
            author = SubFactory(UserFactory)

            class Meta:
                model = Article

        article = ArticleFactory()

        # Testing SubFactory
        self.assertIsInstance(article.author, User)
        self.assertIsInstance(article.author.id, int)
        self.assertIsInstance(article.author.is_staff, bool)
        self.assertIsInstance(article.author.date_joined, datetime)

        # Testing Factory
        self.assertIsInstance(article.id, int)
        self.assertIsInstance(article.slug, str)

        # Testing hooks
        user = article.author
        self.assertTrue(
            hasattr(user, "pre_save_called") and user.pre_save_called
        )
        self.assertTrue(
            hasattr(user, "post_save_called") and user.post_save_called
        )

        # **********************************
        # ******* DjangoModelFactory *******
        # **********************************

        class DjangoUserFactory(DjangoModelFactory):
            id = FACTORY.pyint()
            username = FACTORY.username()
            first_name = FACTORY.first_name()
            last_name = FACTORY.last_name()
            email = FACTORY.email()
            last_login = FACTORY.date_time()
            is_superuser = False
            is_staff = False
            is_active = FACTORY.pybool()
            date_joined = FACTORY.date_time()

            class Meta:
                model = User
                get_or_create = ("username",)

            @staticmethod
            @pre_save
            def __pre_save_method(instance):
                instance.pre_save_called = True

            @staticmethod
            @post_save
            def __post_save_method(instance):
                instance.post_save_called = True

        class DjangoArticleFactory(DjangoModelFactory):
            id = FACTORY.pyint()
            title = FACTORY.sentence()
            slug = FACTORY.slug()
            content = FACTORY.text()
            image = FACTORY.png_file(storage=STORAGE)
            pub_date = FACTORY.date()
            safe_for_work = FACTORY.pybool()
            minutes_to_read = FACTORY.pyint(min_value=1, max_value=10)
            author = SubFactory(DjangoUserFactory)

            class Meta:
                model = Article

            @staticmethod
            @pre_save
            def __pre_save_method(instance):
                instance.pre_save_called = True

            @staticmethod
            @post_save
            def __post_save_method(instance):
                instance.post_save_called = True

        django_article = DjangoArticleFactory(author__username="admin")

        # Testing SubFactory
        self.assertIsInstance(django_article.author, User)
        self.assertIsInstance(django_article.author.id, int)
        self.assertIsInstance(django_article.author.is_staff, bool)
        self.assertIsInstance(django_article.author.date_joined, datetime)

        # Testing Factory
        self.assertIsInstance(django_article.id, int)
        self.assertIsInstance(django_article.slug, str)

        # Testing hooks
        self.assertTrue(
            hasattr(django_article, "pre_save_called")
            and django_article.pre_save_called
        )
        self.assertTrue(
            hasattr(django_article, "post_save_called")
            and django_article.post_save_called
        )

        # Testing batch creation
        django_articles = DjangoArticleFactory.create_batch(5)
        self.assertEqual(len(django_articles), 5)
        self.assertIsInstance(django_articles[0], Article)

    def test_registry_integration(self) -> None:
        """Test `add`."""
        # Create a TXT file.
        txt_file_1 = FAKER.txt_file()

        with self.subTest("Check if `add` works"):
            # Check if `add` works (the file is in the registry)
            self.assertIn(txt_file_1, FILE_REGISTRY._registry)

        with self.subTest("Check if `search` works"):
            # Check if `search` works
            res = FILE_REGISTRY.search(str(txt_file_1))
            self.assertIsNotNone(res)
            self.assertEqual(res, txt_file_1)

        with self.subTest("Check if `remove` by `StringValue` works"):
            # Check if `remove` by `StringValue`.
            FILE_REGISTRY.remove(txt_file_1)
            self.assertNotIn(txt_file_1, FILE_REGISTRY._registry)

        with self.subTest("Check if `remove` by `str` works"):
            # Create another TXT file and check if `remove` by `str` works.
            txt_file_2 = FAKER.txt_file()
            self.assertIn(txt_file_2, FILE_REGISTRY._registry)
            FILE_REGISTRY.remove(str(txt_file_2))
            self.assertNotIn(txt_file_2, FILE_REGISTRY._registry)

        with self.subTest("Check if `clean_up` works"):
            # Check if `clean_up` works
            txt_file_3 = FAKER.txt_file()
            txt_file_4 = FAKER.txt_file()
            txt_file_5 = FAKER.txt_file()
            self.assertIn(txt_file_3, FILE_REGISTRY._registry)
            self.assertIn(txt_file_4, FILE_REGISTRY._registry)
            self.assertIn(txt_file_5, FILE_REGISTRY._registry)

            FILE_REGISTRY.clean_up()
            self.assertNotIn(txt_file_3, FILE_REGISTRY._registry)
            self.assertNotIn(txt_file_4, FILE_REGISTRY._registry)
            self.assertNotIn(txt_file_5, FILE_REGISTRY._registry)

    def test_remove_by_string_not_found(self):
        res = FILE_REGISTRY.remove("i_do_not_exist.ext")
        self.assertFalse(res)

    def test_remove_exceptions(self):
        txt_file = FAKER.txt_file()
        txt_file.data["storage"].unlink(txt_file)

        res = FILE_REGISTRY.remove(txt_file)
        self.assertFalse(res)

    def test_clean_up_exceptions(self):
        # Redirect logger output to a string stream
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        LOGGER.addHandler(handler)
        txt_file = FAKER.txt_file()
        txt_file.data["storage"].unlink(txt_file)

        # Clean up registry
        FILE_REGISTRY.clean_up()

        # Check the content of the logging output
        log_output = log_stream.getvalue()
        self.assertIn(
            f"Failed to unlink file {txt_file.data['filename']}",
            log_output,
        )

        # Clean up by removing the handler
        LOGGER.removeHandler(handler)


if __name__ == "__main__":
    unittest.main()
