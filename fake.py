"""
https://github.com/barseghyanartur/fake.py/
"""

import array
import asyncio
import contextlib
import io
import locale
import logging
import math
import mimetypes
import os
import random
import re
import string
import subprocess
import tarfile
import unittest
import uuid
import wave
import zipfile
import zlib
import zoneinfo
from abc import abstractmethod
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field, fields, is_dataclass
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from email.message import EmailMessage
from email.policy import default
from email.utils import parseaddr
from functools import partial
from inspect import signature
from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile, gettempdir
from threading import Lock
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Sequence,
    Set,
    TextIO,
    Tuple,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)
from unittest.mock import patch
from uuid import UUID

__title__ = "fake.py"
__version__ = "0.9.7"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "AuthorshipData",
    "BaseStorage",
    "CLI",
    "DjangoModelFactory",
    "DocxGenerator",
    "FACTORY",
    "FAKER",
    "FILE_REGISTRY",
    "Factory",
    "FactoryMethod",
    "Faker",
    "FileRegistry",
    "FileSystemStorage",
    "GraphicPdfGenerator",
    "LazyAttribute",
    "LazyFunction",
    "MetaData",
    "ModelFactory",
    "OdtGenerator",
    "PROVIDER_REGISTRY",
    "PostSave",
    "PreInit",
    "PreSave",
    "PydanticModelFactory",
    "SQLAlchemyModelFactory",
    "StringValue",
    "SubFactory",
    "TextPdfGenerator",
    "TortoiseModelFactory",
    "fill_dataclass",
    "fill_pydantic_model",
    "format_type_hint",
    "get_argparse_type",
    "get_provider_args",
    "get_provider_defaults",
    "is_optional_type",
    "main",
    "organize_providers",
    "post_save",
    "pre_init",
    "pre_save",
    "provider",
    "run_async_in_thread",
    "slugify",
    "trait",
    "xor_transform",
)

LOGGER = logging.getLogger(__name__)
T = TypeVar("T")
ElementType = Sequence[T]

# ************************************************
# ******************* Public *********************
# ************************************************

IMAGE_SERVICES = (
    "https://picsum.photos/{width}/{height}",
    "https://dummyimage.com/{width}x{height}",
    "https://placekitten.com/{width}/{height}",
    "https://loremflickr.com/{width}/{height}",
)

FREE_EMAIL_DOMAINS = (
    "gmail.com",
    "hotmail.com",
    "mail.com",
    "outlook.com",
    "proton.me",
    "protonmail.com",
    "yahoo.com",
)

TLDS = (
    "com",
    "org",
    "net",
    "io",
)

URL_PROTOCOLS = (
    "http",
    "https",
)

URL_SUFFIXES = (
    ".html",
    ".php",
    ".go",
    "",
    "/",
)

FILE_TYPES = mimetypes.types_map
FILE_EXTENSIONS = [__v[1:] for __v in FILE_TYPES.keys()]
MIME_TYPES = list(FILE_TYPES.values())

UNWANTED_GEO_PATTERN = re.compile(
    r"^([A-Z0-9-+]+$|GB.*|localtime|Universal|Etc|Factory)"
)

TAR_COMPRESSION_OPTIONS = {"gz", "bz2", "xz"}

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
6 0 obj
<</Type /Font /Subtype /Type1 /BaseFont /Helvetica>>
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


SLUGIFY_RE = re.compile(r"[^a-zA-Z0-9]")


def slugify(value: str) -> str:
    """Slugify."""
    return SLUGIFY_RE.sub("", value).lower()


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

    def __new__(
        cls: Type["StringValue"],
        value: str,
        *args,
        **kwargs,
    ) -> "StringValue":
        obj = str.__new__(cls, value)
        obj.data = {}
        return obj


class BytesValue(bytes):
    data: Dict[str, Any]

    def __new__(
        cls: Type["BytesValue"],
        value: bytes,
        *args,
        **kwargs,
    ) -> "BytesValue":
        obj = bytes.__new__(cls, value)
        obj.data = {}
        return obj


def returns_list(func: Callable) -> bool:
    """Checks if callable returns a list of `StringValue`.

    Returns True if it's a List. Returns False otherwise.
    """
    try:
        return_type = get_type_hints(func).get("return", None)
    except Exception:
        return False

    if not return_type:
        return False

    return_origin = getattr(return_type, "__origin__", None)
    if return_origin is list or return_origin is List:
        # If it's a list, check the type of its elements
        element_type = getattr(return_type, "__args__", [None])[0]
        if element_type in {StringValue, BytesValue}:
            return True
        element_origin = getattr(element_type, "__origin__", None)
        if element_origin is Union:
            if set(getattr(element_type, "__args__", [])) == {
                BytesValue,
                StringValue,
            }:
                return True

    return False


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

    def __init__(self) -> None:
        self._registry: Set[StringValue] = set()
        self._lock = Lock()

    def add(self, string_value: StringValue) -> None:
        with self._lock:
            self._registry.add(string_value)

    def remove(self, string_value: Union[StringValue, str]) -> bool:
        if not isinstance(string_value, StringValue):
            string_value = self.search(string_value)  # type: ignore

        if not string_value:
            return False

        with self._lock:
            # No error if the element doesn't exist
            self._registry.discard(string_value)  # type: ignore
            try:
                string_value.data["storage"].unlink(  # type: ignore
                    string_value.data["filename"]  # type: ignore
                )
                return True
            except Exception as e:
                LOGGER.error(
                    f"Failed to unlink file "
                    f"{string_value.data['filename']}: {e}"  # type: ignore
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

    def generate_basename(
        self: "BaseStorage",
        prefix: str = "tmp",
        length: int = 8,
    ) -> str:
        """Generate a random alphanumeric sequence."""
        if not prefix:
            prefix = "tmp"
        # Use lowercase letters, digits and underscore
        characters = string.ascii_lowercase + string.digits + "_"
        return prefix + "".join(random.choices(characters, k=length))

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

        from fake import FAKER, FileSystemStorage

        storage = FileSystemStorage()
        docx_file = storage.generate_filename(prefix="zzz_", extension="docx")
        storage.write_bytes(docx_file, FAKER.docx())

    Initialization with params:

    .. code-block:: python

        from fake import FAKER, FileSystemStorage

        storage = FileSystemStorage()
        docx_file = FAKER.docx_file(storage=storage)
    """

    def __init__(
        self: "FileSystemStorage",
        root_path: Optional[Union[str, Path]] = gettempdir(),
        rel_path: Optional[str] = "tmp",
        *args,
        **kwargs,
    ) -> None:
        """
        :param root_path: Path of your files root directory (e.g., Django's
            `settings.MEDIA_ROOT`).
        :param rel_path: Relative path (from root directory).
        :param *args:
        :param **kwargs:
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

        if not basename:
            basename = self.generate_basename(prefix)

        return str(dir_path / f"{basename}.{extension}")

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
        from fake import FAKER, TextPdfGenerator

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

        pdf_bytes.write(b"%PDF-1.4\n")
        pdf_bytes.write(b"1 0 obj\n<</Type /Catalog/Pages 3 0 R>>\nendobj\n")
        pdf_bytes.write(b"2 0 obj\n<</Font <</F1 6 0 R>>>>\nendobj\n")
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
        from fake import FAKER, GraphicPdfGenerator

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
        from fake import FAKER

        Path("/tmp/example.docx").write_bytes(
            DocxGenerator(FAKER).create(nb_pages=100)
        )
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
            texts = self.faker.sentences(nb=nb_pages)

        if metadata:
            metadata.add_content(texts)  # type: ignore

        # Construct the main document content
        document_content = DOCX_TPL_DOC_HEADER
        for i, page_text in enumerate(texts):  # type: ignore
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


class OdtGenerator:
    """OdtGenerator - generates an ODT file with text.

    Usage example:

    .. code-block:: python

        from pathlib import Path
        from fake import FAKER

        Path("/tmp/example.odt").write_bytes(
            OdtGenerator(FAKER).create(nb_pages=100)
        )
    """

    def __init__(self, faker: "Faker") -> None:
        self.faker = faker

    def _create_page(self, text: str) -> str:
        return (
            f'<text:p text:style-name="P1">{text}</text:p>'
            f'<text:p style:name="P1" style:family="paragraph" '
            f'style:parent-style-name="Standard">'
            f"<text:line-break/></text:p>"
        )

    def create(
        self,
        nb_pages: Optional[int] = None,
        texts: Optional[List[str]] = None,
        metadata: Optional[MetaData] = None,
    ) -> bytes:
        if not nb_pages and not texts:
            raise ValueError("Either `nb_pages` or `texts` must be provided.")
        if texts:
            nb_pages = len(texts)
        else:
            texts = self.faker.sentences(nb=nb_pages)

        if metadata:
            metadata.add_content(texts)  # type: ignore

        # Prepare the XML content with page breaks
        content_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <office:document-content
     xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
     xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
     xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
     xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
     xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
      <office:body>
        <office:text>
    {"".join(self._create_page(text) for text in texts)}
        </office:text>
      </office:body>
    </office:document-content>"""

        # Prepare the XML for styles (including style for page break)
        styles_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <office:document-styles
     xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
     xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
     xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
     xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0">
      <office:styles>
        <style:style style:name="P1" style:family="paragraph">
          <style:paragraph-properties fo:break-before="page"/>
        </style:style>
      </office:styles>
    </office:document-styles>"""

        # Create the ODT file (ZIP archive)
        odt_bytes = io.BytesIO()
        with zipfile.ZipFile(odt_bytes, "w") as odt:
            # Add the mimetype file (needs to be the first file in the
            # archive and uncompressed)
            odt.writestr(
                "mimetype",
                "application/vnd.oasis.opendocument.text",
                zipfile.ZIP_STORED,
            )
            # Add the content and styles files
            odt.writestr("content.xml", content_xml.encode("utf-8"))
            odt.writestr("styles.xml", styles_xml.encode("utf-8"))
            # Add the manifest file
            odt.writestr(
                "META-INF/manifest.xml",
                """<?xml version="1.0" encoding="UTF-8"?>
    <manifest:manifest
      xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">
      <manifest:file-entry
        manifest:media-type="application/vnd.oasis.opendocument.text"
        manifest:full-path="/"/>
      <manifest:file-entry
        manifest:media-type="text/xml"
        manifest:full-path="content.xml"/>
      <manifest:file-entry
        manifest:media-type="text/xml" manifest:full-path="styles.xml"/>
    </manifest:manifest>""".encode(
                    "utf-8"
                ),
            )

        return odt_bytes.getvalue()


class ProviderRegistryItem(str):
    __slots__ = ("tags",)

    tags: Optional[Tuple[str, ...]]

    def __new__(cls, value, *args, **kwargs):
        obj = str.__new__(cls, value)
        obj.tags = tuple()
        return obj


# Global registry for provider methods
UID_REGISTRY: Dict[str, "Faker"] = {}
ALIAS_REGISTRY: Dict[str, "Faker"] = {}
PROVIDER_REGISTRY: Dict[str, Set[ProviderRegistryItem]] = defaultdict(set)


class Provider:
    def __init__(
        self,
        func: Callable,
        tags: Optional[Tuple[str, ...]] = None,
    ) -> None:
        self.func = func
        self.is_provider = True
        self.registered_name = None
        self.tags = tags

    def __set_name__(self, owner, name):
        module = owner.__module__
        class_name = owner.__name__
        class_qualname = f"{module}.{class_name}"
        self.registered_name = f"{module}.{class_name}.{name}"
        func_name = ProviderRegistryItem(self.func.__name__)
        func_name.tags = self.tags
        PROVIDER_REGISTRY[class_qualname].add(func_name)

    def __get__(self, instance, owner):
        # Return a method bound to the instance or the unbound function
        return self.func.__get__(instance, owner)


def provider(*args: Any, tags: Optional[Tuple[str, ...]] = None) -> Callable:
    # Decorator is used without arguments
    if args and callable(args[0]):
        return Provider(args[0])

    # Decorator is used with arguments
    def wrapper(func: Callable) -> Provider:
        return Provider(func, tags=tags)

    return wrapper


class Faker:
    """fake.py - simplified, standalone alternative with no dependencies.

    ----

    Usage example:

    .. code-block:: python

        from fake import FAKER

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
        from fake import FAKER, TextPdfGenerator, GraphicPdfGenerator

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
        from fake import FAKER

        Path("/tmp/image.png").write_bytes(FAKER.png())

        Path("/tmp/image.svg").write_bytes(FAKER.svg())

        Path("/tmp/image.bmp").write_bytes(FAKER.bmp())

        Path("/tmp/image.gif").write_bytes(FAKER.gif())

    Note, that all image formats accept `size` (default: `(100, 100)`)
    and `color`(default: `(255, 0, 0)`) arguments.
    """

    def __init__(self, alias: Optional[str] = None) -> None:
        self._words: List[str] = []
        self._first_names: List[str] = []
        self._last_names: List[str] = []
        self._cities: List[str] = []
        self._countries: List[str] = []
        self._geo_locations: List[str] = []
        self._country_codes: List[str] = []
        self._locales: List[str] = []

        self.uid = f"{self.__class__.__module__}.{self.__class__.__name__}"
        if alias and alias in ALIAS_REGISTRY:
            LOGGER.warning(
                f"Alias '{alias}' already registered. "
                f"Using '{self.uid}' as alias instead."
            )
            alias = None

        self.alias = alias or self.uid
        if self.uid not in UID_REGISTRY:
            UID_REGISTRY[self.uid] = self
        if self.alias not in ALIAS_REGISTRY:
            ALIAS_REGISTRY[self.alias] = self

        self.load_data()

    def load_data(self):
        self.load_words()
        self.load_names()
        self.load_geo_locations()
        self.load_locales_and_country_codes()

    @staticmethod
    def get_by_uid(uid: str) -> Union["Faker", None]:
        return UID_REGISTRY.get(uid, None)

    @staticmethod
    def get_by_alias(alias: str) -> Union["Faker", None]:
        return ALIAS_REGISTRY.get(alias, None)

    def load_words(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            # Dynamically import 'this' module
            this = __import__("this")

        zen_encoded: str = this.s
        translation_map: Dict[str, str] = {v: k for k, v in this.d.items()}
        zen: str = self._rot13_translate(zen_encoded, translation_map)
        self._words = (
            zen.translate(str.maketrans("", "", string.punctuation))
            .lower()
            .split()
        )

    def load_names(self) -> None:
        authorship_data = AuthorshipData()
        self._first_names = list(authorship_data.first_names)
        self._last_names = list(authorship_data.last_names)

    def load_geo_locations(self) -> None:
        cities: Set[str] = set()
        countries: Set[str] = set()
        geo_locations: Set[str] = set()
        add_city = cities.add
        add_country = countries.add
        add_geo_location = geo_locations.add

        for tz in zoneinfo.available_timezones():
            parts = tz.split("/")
            _parts = []
            for part in parts:
                if part:
                    if not UNWANTED_GEO_PATTERN.match(part):
                        _parts.append(part.replace("_", " "))
            if _parts:
                add_geo_location("/".join(_parts))

            # Ignore single-part entries that match our exclusion pattern
            if len(parts) == 1:
                if not UNWANTED_GEO_PATTERN.match(parts[0]):
                    country = parts[0].replace("_", "")
                    add_country(country)
            # Extract cities for Asia and Europe
            elif parts[0] in ["Asia", "Europe"]:
                if len(parts) > 1:  # Check to ensure there is a second part
                    city = parts[1].replace("_", " ")
                    add_city(city)

        self._cities = list(cities)
        self._countries = list(countries)
        self._geo_locations = list(geo_locations)

    def load_locales_and_country_codes(self) -> None:
        # Fetch all available locales from the system
        _available_locales = locale.locale_alias

        # Filter and clean the list to show more standardized locale names
        _locales = {
            __value.split(".")[0]
            for __key, __value in _available_locales.items()
            if "_" in __value
        }

        # Extract country codes from the locale keys
        _country_codes: Set[str] = set()
        add_country_code = _country_codes.add
        for __key in _locales:
            __parts = __key.split("_")
            if len(__parts) > 1:
                # Get the first two characters of the second part,
                # typically the country code
                __country_code = __parts[1][:2]
                # Add to set to ensure uniqueness
                add_country_code(__country_code.upper())

        self._country_codes = list(_country_codes)
        self._locales = list(_locales)

    @staticmethod
    def _rot13_translate(text: str, translation_map: Dict[str, str]) -> str:
        return "".join([translation_map.get(c, c) for c in text])

    @provider(tags=("Unique",))
    def uuid(self) -> UUID:
        """Generate a UUID."""
        return uuid.uuid4()

    @provider(tags=("Unique",))
    def uuids(self, nb: int = 5) -> List[UUID]:
        """Generate a list of UUIDs."""
        return [uuid.uuid4() for _ in range(nb)]

    @provider(tags=("Person",))
    def first_name(self) -> str:
        """Generate a first name."""
        return random.choice(self._first_names)

    @provider(tags=("Person",))
    def first_names(self, nb: int = 5) -> List[str]:
        """Generate a list of first names."""
        return [self.first_name() for _ in range(nb)]

    @provider(tags=("Person",))
    def last_name(self) -> str:
        """Generate a last name."""
        return random.choice(self._last_names)

    @provider(tags=("Person",))
    def last_names(self, nb: int = 5) -> List[str]:
        """Generate a list of last names."""
        return [self.last_name() for _ in range(nb)]

    @provider(tags=("Person",))
    def name(self) -> str:
        """Generate a name."""
        return f"{self.first_name()} {self.last_name()}"

    @provider(tags=("Person",))
    def names(self, nb: int = 5) -> List[str]:
        """Generate a list of names."""
        return [self.name() for _ in range(nb)]

    @provider(tags=("Person",))
    def username(self) -> str:
        """Generate a username."""
        return (
            f"{self.word()}_{self.word()}_{self.word()}_{self.pystr()}"
        ).lower()

    @provider(tags=("Person",))
    def usernames(self, nb: int = 5) -> List[str]:
        """Generate a list of usernames."""
        return [self.username() for _ in range(nb)]

    @provider(tags=("Text",))
    def slug(self) -> str:
        """Generate a slug."""
        return (
            f"{self.word()}-{self.word()}-{self.word()}-{self.pystr()}"
        ).lower()

    @provider(tags=("Text",))
    def slugs(self, nb: int = 5) -> List[str]:
        """Generate a list of slugs."""
        return [self.slug() for _ in range(nb)]

    @provider(tags=("Text",))
    def word(self) -> str:
        """Generate a word."""
        return random.choice(self._words).capitalize()

    @provider(tags=("Text",))
    def words(self, nb: int = 5) -> List[str]:
        """Generate a list of words."""
        return [word.capitalize() for word in random.choices(self._words, k=nb)]

    @provider(tags=("Text",))
    def sentence(self, nb_words: int = 5) -> str:
        """Generate a sentence."""
        return (
            f"{' '.join([self.word() for _ in range(nb_words)]).capitalize()}."
        )

    @provider(tags=("Text",))
    def sentences(self, nb: int = 3) -> List[str]:
        """Generate a list of sentences."""
        return [self.sentence() for _ in range(nb)]

    @provider(tags=("Text",))
    def paragraph(self, nb_sentences: int = 5) -> str:
        """Generate a paragraph."""
        return " ".join([self.sentence() for _ in range(nb_sentences)])

    @provider(tags=("Text",))
    def paragraphs(self, nb: int = 3) -> List[str]:
        """Generate a list of paragraphs."""
        return [self.paragraph() for _ in range(nb)]

    @provider(tags=("Text",))
    def text(self, nb_chars: int = 200) -> str:
        """Generate a text."""
        current_text: str = ""
        while len(current_text) < nb_chars:
            sentence: str = self.sentence()
            current_text += f" {sentence}" if current_text else sentence
        return current_text[:nb_chars]

    @provider(tags=("Text",))
    def texts(self, nb: int = 3) -> List[str]:
        """Generate a list of texts."""
        return [self.text() for _ in range(nb)]

    @provider(tags=("Filename",))
    def file_name(self, extension: str = "txt") -> str:
        """Generate a random filename."""
        with NamedTemporaryFile(suffix=f".{extension}") as temp_file:
            return temp_file.name

    @provider(tags=("Filename",))
    def file_extension(self) -> str:
        """Generate a random extension."""
        return random.choice(FILE_EXTENSIONS)

    @provider(tags=("Filename",))
    def mime_type(self) -> str:
        """Generate a random mime type."""
        return random.choice(MIME_TYPES)

    @provider(tags=("Internet",))
    def tld(self, tlds: Optional[Tuple[str, ...]] = None) -> str:
        """Generate a random TLD."""
        return random.choice(tlds or TLDS)

    @provider(tags=("Internet",))
    def domain_name(self, tlds: Optional[Tuple[str, ...]] = None) -> str:
        """Generate a random domain name."""
        domain = self.word().lower()
        tld = self.tld(tlds)
        return f"{domain}.{tld}"

    @provider(tags=("Internet",))
    def free_email_domain(self) -> str:
        """Generate a random free email domain."""
        return random.choice(FREE_EMAIL_DOMAINS)

    @provider(tags=("Internet",))
    def email(self, domain_names: Optional[Tuple[str, ...]] = None) -> str:
        """Generate a random email."""
        domain = random.choice(domain_names) if domain_names else None
        return f"{self.word().lower()}@{domain or self.domain_name()}"

    @provider(tags=("Internet",))
    def company_email(
        self,
        domain_names: Optional[Tuple[str, ...]] = None,
    ) -> str:
        """Generate a random company email."""
        domain = random.choice(domain_names) if domain_names else None
        return f"{slugify(self.name())}@{domain or self.domain_name()}"

    @provider(tags=("Internet",))
    def free_email(
        self,
        domain_names: Optional[Tuple[str, ...]] = None,
    ) -> str:
        """Generate a random free email."""
        domain = random.choice(domain_names) if domain_names else None
        return f"{slugify(self.name())}@{domain or self.free_email_domain()}"

    @provider(tags=("Internet",))
    def url(
        self,
        protocols: Optional[Tuple[str, ...]] = None,
        tlds: Optional[Tuple[str, ...]] = None,
        suffixes: Optional[Tuple[str, ...]] = None,
    ) -> str:
        """Generate a random URL."""
        protocol = random.choice(protocols or URL_PROTOCOLS)
        suffix = random.choice(suffixes or URL_SUFFIXES)
        return (
            f"{protocol}://"
            f"{self.domain_name(tlds)}"
            f"/{self.word().lower()}"
            f"{suffix}"
        )

    @provider(tags=("Internet",))
    def image_url(
        self,
        width: int = 800,
        height: int = 600,
        service_url: Optional[str] = None,
    ) -> str:
        """Generate a random image URL."""
        if service_url is None:
            service_url = random.choice(IMAGE_SERVICES)
        return service_url.format(width=width, height=height)

    @provider(tags=("Python",))
    def pyint(self, min_value: int = 0, max_value: int = 9999) -> int:
        """Generate a random integer."""
        return random.randint(min_value, max_value)

    @provider(tags=("Python",))
    def pybool(self) -> bool:
        """Generate a random boolean."""
        return random.choice(
            (
                True,
                False,
            )
        )

    @provider(tags=("Python",))
    def pystr(self, nb_chars: int = 20) -> str:
        """Generate a random string."""
        return "".join(random.choices(string.ascii_letters, k=nb_chars))

    @provider(tags=("Python",))
    def pyfloat(
        self,
        min_value: float = 0.0,
        max_value: float = 10.0,
    ) -> float:
        """Generate a random float number."""
        return random.uniform(min_value, max_value)

    @provider(tags=("Python",))
    def pydecimal(
        self,
        left_digits: int = 5,
        right_digits: int = 2,
        positive: bool = True,
    ) -> Decimal:
        """Generate a random Decimal number.

        :param left_digits: Number of digits to the left of the decimal point.
        :param right_digits: Number of digits to the right of the decimal point.
        :param positive: If True, the number will be positive, otherwise it
            can be negative.
        :return: A randomly generated Decimal number.
        :rtype: Decimal
        :raises: ValueError
        """
        if left_digits < 0:
            raise ValueError("`left_digits` must be at least 0")
        if right_digits < 0:
            raise ValueError("`right_digits` must be at least 0")

        if left_digits > 0:
            # Generate the integer part
            __lower = 10 ** (left_digits - 1)
            __upper = (10**left_digits) - 1
            int_part = random.randint(__lower, __upper)
        else:
            int_part = 0

        if right_digits > 0:
            # Generate the fractional part
            __lower = 10 ** (right_digits - 1)
            __upper = (10**right_digits) - 1
            fractional_part = random.randint(__lower, __upper)
        else:
            fractional_part = 0

        # Combine both parts
        number = Decimal(f"{int_part}.{fractional_part}")

        # Make the number negative if needed
        if not positive:
            number = -number

        return number

    @provider(tags=("Internet",))
    def ipv4(self) -> str:
        """Generate a random IP v4."""
        return ".".join(str(random.randint(0, 255)) for _ in range(4))

    def _parse_date_string(
        self, date_str: str, tzinfo: timezone = timezone.utc
    ) -> datetime:
        """Parse date string with notation below into a datetime object:

        - '5M': 5 minutes from now
        - '-1d': 1 day ago
        - '-1H': 1 hour ago
        - '-365d': 365 days ago

        :param date_str: The date string with shorthand notation.
        :param tzinfo: Timezone info.
        :return: A datetime object representing the time offset.
        :rtype: datetime
        :raises: ValueError
        """
        if date_str in ["now", "today"]:
            return datetime.now(tzinfo)

        match = re.match(r"([+-]?\d+)([dHM])", date_str)
        if not match:
            raise ValueError(
                "Date string format is incorrect. Expected formats like "
                "'-1d', '+2H', '-30M'."
            )
        value, unit = match.groups()
        value = int(value)
        if unit == "d":  # Days
            return datetime.now(tzinfo) + timedelta(days=value)
        elif unit == "H":  # Hours
            return datetime.now(tzinfo) + timedelta(hours=value)

        # Otherwise it's minutes
        return datetime.now(tzinfo) + timedelta(minutes=value)

    @provider(tags=("Date/Time",))
    def date(
        self,
        start_date: str = "-7d",
        end_date: str = "+0d",
        tzinfo: timezone = timezone.utc,
    ) -> date:
        """Generate random date between `start_date` and `end_date`.

        :param start_date: The start date from which the random date should
            be generated in the shorthand notation.
        :param end_date: The end date up to which the random date should be
            generated in the shorthand notation.
        :param tzinfo: The timezone.
        :return: A string representing the formatted date.
        :rtype: date
        """
        start_datetime = self._parse_date_string(start_date, tzinfo)
        end_datetime = self._parse_date_string(end_date, tzinfo)
        time_between_dates = (end_datetime - start_datetime).days
        random_days = random.randrange(
            time_between_dates + 1
        )  # Include the end date
        random_date = start_datetime + timedelta(days=random_days)
        return random_date.date()

    @provider(tags=("Date/Time",))
    def date_time(
        self,
        start_date: str = "-7d",
        end_date: str = "+0d",
        tzinfo: timezone = timezone.utc,
    ) -> datetime:
        """Generate a random datetime between `start_date` and `end_date`.

        :param start_date: The start datetime from which the random datetime
            should be generated in the shorthand notation.
        :param end_date: The end datetime up to which the random datetime
            should be generated in the shorthand notation.
        :param tzinfo: The timezone.
        :return: A string representing the formatted datetime.
        :rtype: datetime
        """
        start_datetime = self._parse_date_string(start_date, tzinfo)
        end_datetime = self._parse_date_string(end_date, tzinfo)
        time_between_datetimes = int(
            (end_datetime - start_datetime).total_seconds()
        )
        random_seconds = random.randrange(
            time_between_datetimes + 1
        )  # Include the end date time
        random_date_time = start_datetime + timedelta(seconds=random_seconds)
        return random_date_time

    @provider(tags=("Document",))
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

    @provider(tags=("Document",))
    def text_pdf(
        self,
        nb_pages: int = 1,
        generator: Type[TextPdfGenerator] = TextPdfGenerator,
        metadata: Optional[MetaData] = None,
        **kwargs,
    ) -> bytes:
        """Create a PDF document of a given size."""
        return self.pdf(
            nb_pages=nb_pages,
            generator=generator,
            metadata=metadata,
            **kwargs,
        )

    @provider(tags=("Image",))
    def png(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
    ) -> bytes:
        """Create a PNG image of a specified size and color.

        :param size: Tuple of width and height of the image in pixels.
        :param color: Color of the image in RGB format (tuple of three
            integers).
        :return: Byte content of the PNG image.
        :rtype: bytes
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
                length=4,
                byteorder="big",
            )
        )

        # IEND chunk: marks the image end
        iend_chunk = b"\x00\x00\x00\x00IEND\xAE\x42\x60\x82"

        # Combine all chunks
        png_data = png_header + ihdr_chunk + idat_chunk + iend_chunk

        return png_data

    @provider(tags=("Image",))
    def svg(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
    ) -> bytes:
        """Create an SVG image of a specified size and color.

        :param size: Tuple of width and height of the image in pixels.
        :param color: Color of the image in RGB format (tuple of three
            integers).
        :return: Byte content of the SVG image.
        :rtype: bytes
        """
        width, height = size
        return SVG_TPL.format(width=width, height=height, color=color).encode()

    @provider(tags=("Image",))
    def bmp(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
    ) -> bytes:
        """Create a BMP image of a specified size and color.

        :param size: Tuple of width and height of the image in pixels.
        :param color: Color of the image in RGB format (tuple of three
            integers).
        :return: Byte content of the BMP image.
        :rtype: bytes
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

    @provider(tags=("Image",))
    def gif(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
    ) -> bytes:
        """Create a GIF image of a specified size and color.

        :param size: Tuple of width and height of the image in pixels.
        :param color: Color of the image in RGB format (tuple of three
            integers).
        :return: Byte content of the GIF image.
        :rtype: bytes
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

    @provider(tags=("Image",))
    def tif(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
    ) -> bytes:
        """Create a TIF image of a specified size and color.

        :param size: Tuple of width and height of the image in pixels.
        :param color: Color of the image in RGB format (tuple of three
            integers).
        :return: Byte content of the TIF image.
        :rtype: bytes
        """
        width, height = size
        r, g, b = color
        # TIFF Header
        # Byte order indication ('II' for little endian)
        # Version number (42)
        # Offset to the first IFD (8 bytes from the beginning)
        tiff_header = b"II\x2A\x00\x08\x00\x00\x00"

        # IFD setup
        num_entries = 12
        ifd_offset = 8
        next_ifd = 0  # No next IFD

        # Image data starting just after IFD
        # (8 bytes for header + 2 + 12*num_entries + 4 for next IFD)
        data_offset = ifd_offset + 2 + 12 * num_entries + 4

        # Entries in IFD
        entries = [
            (256, 4, 1, width),  # Image width
            (257, 4, 1, height),  # Image height
            (258, 3, 3, data_offset + width * height * 3),  # Bits per sample
            (259, 3, 1, 1),  # Compression (1 = no compression)
            (262, 3, 1, 2),  # Photometric interpretation (2 = RGB)
            (273, 4, 1, data_offset),  # Offset to image data
            (277, 3, 1, 3),  # Samples per pixel
            (278, 4, 1, height),  # Rows per strip
            (279, 4, 1, width * height * 3),
            # Strip byte counts (image data size)
            (282, 5, 1, data_offset + width * height * 3 + 6),
            # XResolution placeholder offset
            (283, 5, 1, data_offset + width * height * 3 + 14),
            # YResolution placeholder offset
            (284, 3, 1, 1),  # Planar configuration (1 = chunky)
        ]

        # Write IFD
        ifd = bytearray()
        ifd += int.to_bytes(num_entries, 2, "little")
        for entry in entries:
            tag, type_, count, value = entry
            ifd += int.to_bytes(tag, 2, "little")
            ifd += int.to_bytes(type_, 2, "little")
            ifd += int.to_bytes(count, 4, "little")
            ifd += int.to_bytes(value, 4, "little")
        ifd += int.to_bytes(next_ifd, 4, "little")

        # Image data
        image_data = bytes([r, g, b] * width * height)

        # Bits per sample values (8 bits per channel)
        bits_per_sample = bytes([8, 0, 8, 0, 8, 0])

        # Resolution (72 dpi, stored as a rational number 72/1)
        resolution = (72, 1)
        res_bytes = int.to_bytes(resolution[0], 4, "little")
        res_bytes += int.to_bytes(resolution[1], 4, "little")
        res_bytes += res_bytes  # For both X and Y resolutions

        # Complete TIFF file
        return tiff_header + ifd + image_data + bits_per_sample + res_bytes

    @provider(tags=("Image",))
    def ppm(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
    ) -> bytes:
        """Create a PPM image of a specified size and color.

        :param size: Tuple of width and height of the image in pixels.
        :param color: Color of the image in RGB format, tuple of three
            integers: (0-255, 0-255, 0-255).
        :return: Byte content of the PPM image.
        :rtype: bytes
        """
        width, height = size

        # PPM Header
        ppm_header = f"P6\n{width} {height}\n255\n".encode()

        # Image data
        image_data = bytearray()
        for _ in range(height):
            for _ in range(width):
                image_data.extend(color)

        # Complete PPM file
        return ppm_header + bytes(image_data)

    @provider(tags=("Image",))
    def image(
        self,
        image_format: Literal[
            "png",
            "svg",
            "bmp",
            "gif",
            "tif",
            "ppm",
        ] = "png",
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
    ) -> bytes:
        """Create an image of a specified format, size and color."""
        if image_format not in {"png", "svg", "bmp", "gif", "tif", "ppm"}:
            raise ValueError()
        image_func = getattr(self, image_format)
        return image_func(size=size, color=color)

    @provider(tags=("Audio",))
    def wav(
        self,
        frequency: int = 440,
        duration: int = 1,
        volume: Union[float, int] = 0.5,
        sample_rate: int = 44100,
    ) -> bytes:
        """Create a WAV audio.

        :param frequency: The frequency of the tone in Hz.
        :param duration: Duration of the tone in seconds.
        :param volume: Volume of the tone, scale between 0.0 and 1.0.
        :param sample_rate: Sampling rate in Hz.
        :return: Byte content of the WAV audio.
        :rtype: bytes
        """
        num_samples = int(sample_rate * duration)
        samples_per_cycle = int(sample_rate / frequency)
        cycle = array.array(
            "h"
        )  # 'h' is the typecode for signed short integers

        # Precompute one cycle of the sine wave
        for i in range(samples_per_cycle):
            sample = (
                volume * 32767 * math.sin(2 * math.pi * i / samples_per_cycle)
            )
            cycle.append(int(sample))

        # Generate full data by repeating the cycle
        data = (cycle * (1 + num_samples // samples_per_cycle))[:num_samples]

        # Prepare WAV file structure in a BytesIO stream
        buffer = io.BytesIO()
        with wave.open(buffer, "w") as _wav_file:
            _wav_file.setnchannels(1)  # Mono
            _wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
            _wav_file.setframerate(sample_rate)
            _wav_file.writeframes(data.tobytes())

        # Get the bytes
        wav_bytes = buffer.getvalue()
        buffer.close()

        return wav_bytes

    @provider(tags=("Document",))
    def docx(
        self,
        nb_pages: Optional[int] = 1,
        texts: Optional[List[str]] = None,
        metadata: Optional[MetaData] = None,
    ) -> bytes:
        """Create a DOCX document."""
        _docx = DocxGenerator(faker=self)
        return _docx.create(nb_pages=nb_pages, texts=texts, metadata=metadata)

    @provider(tags=("Document",))
    def odt(
        self,
        nb_pages: Optional[int] = 1,
        texts: Optional[List[str]] = None,
        metadata: Optional[MetaData] = None,
    ) -> bytes:
        """Create a ODT document."""
        _odt = OdtGenerator(faker=self)
        return _odt.create(nb_pages=nb_pages, texts=texts, metadata=metadata)

    @provider(tags=("Binary",))
    def bin(
        self,
        length: int = 16,
    ) -> bytes:
        """Create random bytes."""
        return os.urandom(length)

    @provider(tags=("Archive",))
    def zip(self, options: Optional[Dict[str, Any]] = None, **kwargs):
        """Create a ZIP archive file as bytes.

        Usage example. A complex case.

        .. code-block:: python

            from fake import create_inner_txt_file, FAKER

            zip_file = FAKER.zip(
                prefix="zzz_archive_",
                options={
                    "count": 5,
                    "create_inner_file_func": create_inner_txt_file,
                    "create_inner_file_args": {
                        "prefix": "zzz_file_",
                    },
                    "directory": "zzz",
                },
            )
        """
        data: Dict[str, Any] = {
            "inner": {},
            "files": [],
        }
        fs_storage = FileSystemStorage()

        # Specific
        if options:
            # Complex case
            _count = options.get("count", 1)
            _create_inner_file_func = options.get(
                "create_inner_file_func", create_inner_txt_file
            )
            _create_inner_file_args = options.get("create_inner_file_args", {})
            _dir_path = Path("")
            _directory = options.get("directory", "")

        else:
            # Defaults
            _count = 1
            _create_inner_file_func = create_inner_txt_file
            _create_inner_file_args = {}
            _dir_path = Path("")
            _directory = ""

        _zip_content = BytesIO()
        with zipfile.ZipFile(_zip_content, "w") as __fake_file:
            _kwargs = {}
            _kwargs.update(_create_inner_file_args)

            # If _create_inner_file_func returns a list of values
            if returns_list(_create_inner_file_func):
                _files = _create_inner_file_func(
                    storage=fs_storage,
                    **_kwargs,
                )
                for __file in _files:
                    data["inner"][str(__file)] = __file
                    __file_abs_path = fs_storage.abspath(__file)
                    __fake_file.write(
                        __file_abs_path,
                        arcname=Path(_directory) / Path(__file).name,
                    )
                    os.remove(__file_abs_path)  # Clean up temporary files
                    data["files"].append(Path(_directory) / Path(__file).name)

            # If _create_inner_file_func returns a single value
            else:
                for __i in range(_count):
                    __file = _create_inner_file_func(
                        storage=fs_storage,
                        **_kwargs,
                    )
                    data["inner"][str(__file)] = __file
                    __file_abs_path = fs_storage.abspath(__file)
                    __fake_file.write(
                        __file_abs_path,
                        arcname=Path(_directory) / Path(__file).name,
                    )
                    os.remove(__file_abs_path)  # Clean up temporary files
                    data["files"].append(Path(_directory) / Path(__file).name)

        raw_content = BytesValue(_zip_content.getvalue())
        raw_content.data = data
        return raw_content

    @provider(tags=("Archive",))
    def tar(
        self,
        options: Optional[Dict[str, Any]] = None,
        compression: Optional[Literal["gz", "bz2", "xz"]] = None,
        **kwargs,
    ) -> BytesValue:
        """Generate a TAR archive file as bytes.

        :param options: Options (non-structured) for complex types, such as
            ZIP.
        :param compression: Desired compression. Can be None or `gz`, `bz2`
            or `xz`.
        :param **kwargs: Additional keyword arguments to pass to the function.
        :rtype: BytesValue
        :return: Relative path (from root directory) of the generated file
            or raw content of the file.

        Usage example. Complex case.

        .. code-block:: python

            from fake import create_inner_txt_file, FAKER

            tar_file = FAKER.tar(
                prefix="ttt_archive_",
                options={
                    "count": 5,
                    "create_inner_file_func": create_inner_txt_file,
                    "create_inner_file_args": {
                        "prefix": "ttt_file_",
                    },
                    "directory": "ttt",
                },
            )
        """
        data: Dict[str, Any] = {
            "inner": {},
            "files": [],
        }
        fs_storage = FileSystemStorage()

        # Specific
        if options:
            # Complex case
            _count = options.get("count", 1)
            _create_inner_file_func = options.get(
                "create_inner_file_func", create_inner_txt_file
            )
            _create_inner_file_args = options.get("create_inner_file_args", {})
            _dir_path = Path("")
            _directory = options.get("directory", "")

        else:
            # Defaults
            _count = 1
            _create_inner_file_func = create_inner_txt_file
            _create_inner_file_args = {}
            _dir_path = Path("")
            _directory = ""

        _tar_content = BytesIO()
        _mode = "w"
        if compression and compression in TAR_COMPRESSION_OPTIONS:
            _mode += f":{compression}"
        with tarfile.open(fileobj=_tar_content, mode=_mode) as __fake_file:
            _kwargs = {}
            _kwargs.update(_create_inner_file_args)

            # If _create_inner_file_func returns a list of values
            if returns_list(_create_inner_file_func):
                _files = _create_inner_file_func(
                    storage=fs_storage,
                    **_kwargs,
                )
                for __file in _files:
                    data["inner"][str(__file)] = __file
                    __file_abs_path = fs_storage.abspath(__file)
                    __fake_file.add(
                        __file_abs_path,
                        arcname=Path(_directory) / Path(__file).name,
                    )
                    os.remove(__file_abs_path)  # Clean up temporary files
                    data["files"].append(Path(_directory) / Path(__file).name)

            # If _create_inner_file_func returns a single value
            else:
                for __i in range(_count):
                    __file = _create_inner_file_func(
                        storage=fs_storage,
                        **_kwargs,
                    )
                    data["inner"][str(__file)] = __file
                    __file_abs_path = fs_storage.abspath(__file)
                    __fake_file.add(
                        __file_abs_path,
                        arcname=Path(_directory) / Path(__file).name,
                    )
                    os.remove(__file_abs_path)  # Clean up temporary files
                    data["files"].append(Path(_directory) / Path(__file).name)

        raw_content = BytesValue(_tar_content.getvalue())
        raw_content.data = data
        return raw_content

    @provider(
        tags=(
            "Archive",
            "Email",
        )
    )
    def eml(
        self,
        options: Optional[Dict[str, Any]] = None,
        content: Optional[str] = None,
        subject: Optional[str] = None,
        **kwargs,
    ) -> BytesValue:
        """Generate an EML file bytes.

        :param options: Options (non-structured) for complex types, such as
            ZIP.
        :param content: Email body text.
        :param subject: Email subject.
        :param **kwargs: Additional keyword arguments to pass to the function.
        :rtype: BytesValue
        :return: Relative path (from root directory) of the generated file
            or raw content of the file.

        Usage example. A complex case.

        .. code-block:: python

            from fake import create_inner_docx_file, FAKER

            eml_file = FAKER.eml_file(
                prefix="zzz_email_",
                options={
                    "count": 5,
                    "create_inner_file_func": create_inner_docx_file,
                    "create_inner_file_args": {
                        "prefix": "zzz_file_",
                    },
                }
            )
        """
        fs_storage = FileSystemStorage()

        if not content:
            content = self.text()
        if not subject:
            subject = self.sentence()
        data: Dict[str, Any] = {
            "content": f"{subject}\n {content}",
            "inner": {},
        }

        msg = EmailMessage()
        msg["To"] = self.email()
        msg["From"] = self.email()
        msg["Subject"] = subject
        msg.set_content(content)
        data.update(
            {
                "to": msg["To"],
                "from": msg["From"],
                "subject": msg["Subject"],
                "body": content,
            }
        )

        # Specific
        if options:
            # Complex case
            _count = options.get("count", 1)
            _create_inner_file_func = options.get("create_inner_file_func")
            _create_inner_file_args = options.get("create_inner_file_args", {})

        else:
            # Defaults
            _count = 1
            _create_inner_file_func = None
            _create_inner_file_args = {}

        _kwargs = {}
        _kwargs.update(_create_inner_file_args)

        if _create_inner_file_func and callable(_create_inner_file_func):
            # If _create_inner_file_func returns a list of values
            if returns_list(_create_inner_file_func):
                _files = _create_inner_file_func(
                    storage=fs_storage,
                    **_kwargs,
                )
                for __file in _files:
                    data["inner"][str(__file)] = __file
                    __file_abs_path = fs_storage.abspath(__file)
                    _content_type = "application/octet-stream"
                    _maintype, _subtype = _content_type.split("/", 1)
                    with open(__file_abs_path, "rb") as _fp:
                        _file_data = _fp.read()
                        msg.add_attachment(
                            _file_data,
                            maintype=_maintype,
                            subtype=_subtype,
                            filename=os.path.basename(__file),
                        )
                    os.remove(__file_abs_path)  # Clean up temporary files
            # If _create_inner_file_func returns a single value
            else:
                for __i in range(_count):
                    __file = _create_inner_file_func(
                        storage=fs_storage,
                        **_kwargs,
                    )
                    data["inner"][str(__file)] = __file
                    __file_abs_path = fs_storage.abspath(__file)
                    _content_type = "application/octet-stream"
                    _maintype, _subtype = _content_type.split("/", 1)
                    with open(__file_abs_path, "rb") as _fp:
                        _file_data = _fp.read()
                        msg.add_attachment(
                            _file_data,
                            maintype=_maintype,
                            subtype=_subtype,
                            filename=os.path.basename(__file),
                        )
                    os.remove(__file_abs_path)  # Clean up temporary files

        raw_content = BytesValue(msg.as_bytes(policy=default))
        raw_content.data = data
        return raw_content

    @provider(
        tags=(
            "Document",
            "File",
        )
    )
    def pdf_file(
        self,
        nb_pages: int = 1,
        generator: Union[
            Type[TextPdfGenerator], Type[GraphicPdfGenerator]
        ] = GraphicPdfGenerator,
        metadata: Optional[MetaData] = None,
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
        **kwargs,
    ) -> StringValue:
        """Create a PDF file."""
        if storage is None:
            storage = FileSystemStorage()
        filename = storage.generate_filename(
            extension="pdf",
            prefix=prefix,
            basename=basename,
        )
        if not metadata:
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

    @provider(
        tags=(
            "Document",
            "File",
        )
    )
    def text_pdf_file(
        self,
        nb_pages: int = 1,
        generator: Type[TextPdfGenerator] = TextPdfGenerator,
        metadata: Optional[MetaData] = None,
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
        **kwargs,
    ) -> StringValue:
        """Create a text PDF file."""
        return self.pdf_file(
            nb_pages=nb_pages,
            generator=generator,
            metadata=metadata,
            storage=storage,
            basename=basename,
            prefix=prefix,
            **kwargs,
        )

    def _image_file(
        self,
        image_format: Literal[
            "png",
            "svg",
            "bmp",
            "gif",
            "tif",
            "ppm",
        ] = "png",
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
        extension: Optional[str] = None,
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
    ) -> StringValue:
        if storage is None:
            storage = FileSystemStorage()
        if extension is None:
            extension = image_format
        filename = storage.generate_filename(
            extension=extension,
            prefix=prefix,
            basename=basename,
        )
        data = self.image(image_format=image_format, size=size, color=color)
        storage.write_bytes(filename=filename, data=data)
        file = StringValue(storage.relpath(filename))
        file.data = {"storage": storage, "filename": filename}
        FILE_REGISTRY.add(file)
        return file

    @provider(
        tags=(
            "Image",
            "File",
        )
    )
    def png_file(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
        extension: Optional[str] = None,
    ) -> StringValue:
        """Create a PNG image file of a specified size and color."""
        return self._image_file(
            image_format="png",
            size=size,
            color=color,
            storage=storage,
            basename=basename,
            prefix=prefix,
            extension=extension,
        )

    @provider(
        tags=(
            "Image",
            "File",
        )
    )
    def svg_file(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
        extension: Optional[str] = None,
    ) -> StringValue:
        """Create an SVG image file of a specified size and color."""
        return self._image_file(
            image_format="svg",
            size=size,
            color=color,
            storage=storage,
            basename=basename,
            prefix=prefix,
            extension=extension,
        )

    @provider(
        tags=(
            "Image",
            "File",
        )
    )
    def bmp_file(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
        extension: Optional[str] = None,
    ) -> StringValue:
        """Create a BMP image file of a specified size and color."""
        return self._image_file(
            image_format="bmp",
            size=size,
            color=color,
            storage=storage,
            basename=basename,
            prefix=prefix,
            extension=extension,
        )

    @provider(
        tags=(
            "Image",
            "File",
        )
    )
    def gif_file(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
        extension: Optional[str] = None,
    ) -> StringValue:
        """Create a GIF image file of a specified size and color."""
        return self._image_file(
            image_format="gif",
            size=size,
            color=color,
            storage=storage,
            basename=basename,
            prefix=prefix,
            extension=extension,
        )

    @provider(
        tags=(
            "Image",
            "File",
        )
    )
    def tif_file(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
        extension: Optional[str] = None,
    ) -> StringValue:
        """Create a TIF image file of a specified size and color."""
        return self._image_file(
            image_format="tif",
            size=size,
            color=color,
            extension=extension,
            storage=storage,
            basename=basename,
            prefix=prefix,
        )

    @provider(
        tags=(
            "Image",
            "File",
        )
    )
    def ppm_file(
        self,
        size: Tuple[int, int] = (100, 100),
        color: Tuple[int, int, int] = (0, 0, 255),
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
        extension: Optional[str] = None,
    ) -> StringValue:
        """Create a PPM image file of a specified size and color."""
        return self._image_file(
            image_format="ppm",
            size=size,
            color=color,
            extension=extension,
            storage=storage,
            basename=basename,
            prefix=prefix,
        )

    @provider(
        tags=(
            "Audio",
            "File",
        )
    )
    def wav_file(
        self,
        frequency: int = 440,
        duration: int = 1,
        volume: Union[float, int] = 0.5,
        sample_rate: int = 44100,
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
    ) -> StringValue:
        """Create a WAV audio file."""
        if storage is None:
            storage = FileSystemStorage()
        filename = storage.generate_filename(
            extension="wav",
            prefix=prefix,
            basename=basename,
        )
        data = self.wav(
            frequency=frequency,
            duration=duration,
            volume=volume,
            sample_rate=sample_rate,
        )
        storage.write_bytes(filename=filename, data=data)
        file = StringValue(storage.relpath(filename))
        file.data = {
            "storage": storage,
            "filename": filename,
        }
        FILE_REGISTRY.add(file)
        return file

    @provider(
        tags=(
            "Document",
            "File",
        )
    )
    def docx_file(
        self,
        nb_pages: int = 1,
        texts: Optional[List[str]] = None,
        metadata: Optional[MetaData] = None,
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
    ) -> StringValue:
        """Create a DOCX document file."""
        if storage is None:
            storage = FileSystemStorage()
        filename = storage.generate_filename(
            extension="docx",
            prefix=prefix,
            basename=basename,
        )
        if not metadata:
            metadata = MetaData()
        data = self.docx(nb_pages=nb_pages, texts=texts, metadata=metadata)
        storage.write_bytes(filename=filename, data=data)
        file = StringValue(storage.relpath(filename))
        file.data = {
            "storage": storage,
            "filename": filename,
            "content": metadata.content,
        }
        FILE_REGISTRY.add(file)
        return file

    @provider(
        tags=(
            "Document",
            "File",
        )
    )
    def odt_file(
        self,
        nb_pages: int = 1,
        texts: Optional[List[str]] = None,
        metadata: Optional[MetaData] = None,
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
    ) -> StringValue:
        """Create a ODT document file."""
        if storage is None:
            storage = FileSystemStorage()
        filename = storage.generate_filename(
            extension="odt",
            prefix=prefix,
            basename=basename,
        )
        if not metadata:
            metadata = MetaData()
        data = self.odt(nb_pages=nb_pages, texts=texts, metadata=metadata)
        storage.write_bytes(filename=filename, data=data)
        file = StringValue(storage.relpath(filename))
        file.data = {
            "storage": storage,
            "filename": filename,
            "content": metadata.content,
        }
        FILE_REGISTRY.add(file)
        return file

    @provider(
        tags=(
            "Binary",
            "File",
        )
    )
    def bin_file(
        self,
        length: int = 16,
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
        **kwargs,
    ) -> StringValue:
        """Create a BIN file."""
        if storage is None:
            storage = FileSystemStorage()
        filename = storage.generate_filename(
            extension="bin",
            prefix=prefix,
            basename=basename,
        )
        data = self.bin(length=length)
        storage.write_bytes(filename=filename, data=data)
        file = StringValue(storage.relpath(filename))
        file.data = {
            "storage": storage,
            "filename": filename,
        }
        FILE_REGISTRY.add(file)
        return file

    @provider(
        tags=(
            "Archive",
            "File",
        )
    )
    def zip_file(
        self,
        metadata: Optional[MetaData] = None,
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> StringValue:
        """Create a ZIP archive file."""
        if storage is None:
            storage = FileSystemStorage()
        filename = storage.generate_filename(
            extension="zip",
            prefix=prefix,
            basename=basename,
        )
        if not metadata:
            metadata = MetaData()
        data = self.zip(metadata=metadata, options=options)
        storage.write_bytes(filename=filename, data=data)
        file = StringValue(storage.relpath(filename))
        file.data = {
            "storage": storage,
            "filename": filename,
            "content": metadata.content,
        }
        FILE_REGISTRY.add(file)
        return file

    @provider(
        tags=(
            "Archive",
            "File",
        )
    )
    def tar_file(
        self,
        metadata: Optional[MetaData] = None,
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        compression: Optional[Literal["gz", "bz2", "xz"]] = None,
        **kwargs,
    ) -> StringValue:
        """Create a TAR archive file."""
        if storage is None:
            storage = FileSystemStorage()
        filename = storage.generate_filename(
            extension="tar",
            prefix=prefix,
            basename=basename,
        )
        if not metadata:
            metadata = MetaData()
        data = self.tar(
            metadata=metadata,
            options=options,
            compression=compression,
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

    @provider(
        tags=(
            "Archive",
            "Email",
            "File",
        )
    )
    def eml_file(
        self,
        metadata: Optional[MetaData] = None,
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        content: Optional[str] = None,
        subject: Optional[str] = None,
        **kwargs,
    ) -> StringValue:
        """Create an EML file."""
        if storage is None:
            storage = FileSystemStorage()
        filename = storage.generate_filename(
            extension="eml",
            prefix=prefix,
            basename=basename,
        )
        if not metadata:
            metadata = MetaData()
        data = self.eml(
            metadata=metadata,
            options=options,
            content=content,
            subject=subject,
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

    @provider(
        tags=(
            "Text",
            "File",
        )
    )
    def txt_file(
        self,
        nb_chars: Optional[int] = 200,
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
        text: Optional[str] = None,
    ) -> StringValue:
        """Create a text document file."""
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
        storage.write_text(filename=filename, data=text)  # type: ignore
        file = StringValue(storage.relpath(filename))
        file.data = {
            "storage": storage,
            "filename": filename,
            "content": text,
        }
        FILE_REGISTRY.add(file)
        return file

    @provider(tags=("File",))
    def generic_file(
        self,
        content: Union[bytes, str],
        extension: str,
        storage: Optional[BaseStorage] = None,
        basename: Optional[str] = None,
        prefix: Optional[str] = None,
    ) -> StringValue:
        """Create a generic file."""
        if storage is None:
            storage = FileSystemStorage()
        filename = storage.generate_filename(
            extension=extension,
            prefix=prefix,
            basename=basename,
        )

        if isinstance(content, bytes):
            storage.write_bytes(filename, content)
        else:
            storage.write_text(filename, content)

        file = StringValue(storage.relpath(filename))
        file.data = {
            "content": content,
            "filename": filename,
            "storage": storage,
        }
        FILE_REGISTRY.add(file)
        return file

    @provider(tags=("Geographic",))
    def city(self) -> str:
        """Get a random city."""
        return random.choice(self._cities)

    @provider(tags=("Geographic",))
    def country(self) -> str:
        """Get a random country."""
        return random.choice(self._countries)

    @provider(tags=("Geographic",))
    def geo_location(self) -> str:
        """Get a random geo-location."""
        return random.choice(self._geo_locations)

    @provider(tags=("Geographic",))
    def country_code(self) -> str:
        """Get a random country code."""
        return random.choice(self._country_codes)

    @provider(tags=("Geographic",))
    def locale(self) -> str:
        """Get a random locale."""
        return random.choice(self._locales)

    @provider(tags=("Geographic",))
    def latitude(self) -> float:
        """Generate a random latitude."""
        return random.uniform(-90, 90)

    lat = latitude  # noqa

    @provider(tags=("Geographic",))
    def longitude(self) -> float:
        """Generate a random longitude."""
        return random.uniform(-180, 180)

    lng = lon = longitude  # noqa

    @provider(tags=("Geographic",))
    def latitude_longitude(self) -> Tuple[float, float]:
        """Generate a random (latitude, longitude) pair."""
        return random.uniform(-90, 90), random.uniform(-180, 180)

    latlng = latlon = latitude_longitude  # noqa

    @provider(tags=("Banking",))
    def iban(
        self,
        country_code: Optional[str] = None,
        bank_length: int = 8,
        account_length: int = 10,
    ) -> str:
        """Generate a random valid IBAN number."""
        if not country_code:
            country_code = random.choice(self._country_codes)

        # Generate the bank number and account number
        bank_number = "".join(
            str(random.randint(0, 9)) for _ in range(bank_length)
        )
        account_number = "".join(
            str(random.randint(0, 9)) for _ in range(account_length)
        )

        # Basic Bank Account Number (BBAN)
        bban = bank_number + account_number

        # Convert country code and calculate checksum
        country_number = "".join(
            str(ord(c) - 55) for c in country_code
        )  # Convert letters to numbers
        # Temporary IBAN for checksum calculation
        temporary_iban = bban + country_number + "00"

        # Calculate the checksum using modulo 97
        checksum = 98 - (int(temporary_iban) % 97)
        # Format checksum to be two digits
        checksum_str = f"{checksum:02d}"

        # Construct the actual IBAN
        iban = f"{country_code}{checksum_str}{bban}"

        return iban

    def _calculate_isbn10_checksum(self, digits: str) -> str:
        """Calculate ISBN-10 checksum using correct modulo 11 calculation."""
        weights = range(10, 1, -1)  # Weights from 10 to 2
        total = sum(w * int(d) for w, d in zip(weights, digits))
        remainder = total % 11
        checksum = "X" if remainder == 1 else str((11 - remainder) % 11)
        return checksum

    @provider(tags=("Book",))
    def isbn10(self):
        """Generate a random valid ISBN-10."""
        # Randomly generate the first 9 digits as a string
        digits = "".join(str(random.randint(0, 9)) for _ in range(9))
        # Calculate the checksum digit
        checksum = self._calculate_isbn10_checksum(digits)
        # Form the full ISBN-10 number
        isbn10 = digits + checksum
        # Example format: 'XXX-XXX-XXX-X', commonly used in ISBN
        return f"{isbn10[:3]}-{isbn10[3:6]}-{isbn10[6:9]}-{isbn10[9]}"

    def _isbn13_checksum(self, digits: List[str]) -> str:
        """Calculate the ISBN-13 checksum digit."""
        total = sum(
            (3 if i % 2 else 1) * int(digit) for i, digit in enumerate(digits)
        )
        checksum = (10 - (total % 10)) % 10
        return str(checksum)

    @provider(tags=("Book",))
    def isbn13(self) -> str:
        """Generate a random valid ISBN-13, starting with 978 or 979."""
        prefix = random.choice(["978", "979"])
        digits = [str(random.randint(0, 9)) for _ in range(9)]
        full_digits = list(prefix) + digits
        checksum = self._isbn13_checksum(full_digits)
        isbn = "".join(full_digits) + checksum
        return f"{isbn[0:3]}-{isbn[3:4]}-{isbn[4:7]}-{isbn[7:12]}-{isbn[12]}"

    @provider(tags=("Choice",))
    def random_choice(self, elements: ElementType[T]) -> T:
        return random.choice(elements)

    random_element = random_choice  # noqa

    @provider(tags=("Choice",))
    def random_sample(self, elements: ElementType[T], length: int) -> List[T]:
        return random.sample(elements, length)

    random_elements = random_sample  # noqa

    @provider(tags=("Text",))
    def randomise_string(
        self,
        value: str,
        letters: str = string.ascii_uppercase,
        digits: str = string.digits,
    ) -> str:
        result = ""
        for char in value:
            if char == "?":
                result += random.choice(letters)
            elif char == "#":
                result += random.choice(digits)
            else:
                result += char
        return result

    randomize_string = bothify = randomise_string  # noqa


FAKER = Faker(alias="default")


def create_inner_pdf_file(
    storage: Optional[BaseStorage] = None,
    basename: Optional[str] = None,
    prefix: Optional[str] = None,
    nb_pages: Optional[int] = 1,
    generator: Union[
        Type[TextPdfGenerator], Type[GraphicPdfGenerator]
    ] = GraphicPdfGenerator,
    metadata: Optional[MetaData] = None,
    **kwargs,
) -> StringValue:
    """Create inner PDF file."""
    return FAKER.pdf_file(
        storage=storage,
        basename=basename,
        prefix=prefix,
        nb_pages=nb_pages,
        generator=generator,
        metadata=metadata,
        **kwargs,
    )


def create_inner_text_pdf_file(
    storage: Optional[BaseStorage] = None,
    basename: Optional[str] = None,
    prefix: Optional[str] = None,
    nb_pages: Optional[int] = 1,
    generator: Type[TextPdfGenerator] = TextPdfGenerator,
    metadata: Optional[MetaData] = None,
    **kwargs,
) -> StringValue:
    """Create inner text PDF file."""
    return FAKER.text_pdf_file(
        storage=storage,
        basename=basename,
        prefix=prefix,
        nb_pages=nb_pages,
        generator=generator,
        metadata=metadata,
        **kwargs,
    )


def create_inner_png_file(
    storage: Optional[BaseStorage] = None,
    basename: Optional[str] = None,
    prefix: Optional[str] = None,
    size: Tuple[int, int] = (100, 100),
    color: Tuple[int, int, int] = (0, 0, 255),
    **kwargs,
) -> StringValue:
    """Create inner PNG file."""
    return FAKER.png_file(
        storage=storage,
        basename=basename,
        prefix=prefix,
        size=size,
        color=color,
        **kwargs,
    )


def create_inner_svg_file(
    storage: Optional[BaseStorage] = None,
    basename: Optional[str] = None,
    prefix: Optional[str] = None,
    size: Tuple[int, int] = (100, 100),
    color: Tuple[int, int, int] = (0, 0, 255),
    **kwargs,
) -> StringValue:
    """Create inner SVG file."""
    return FAKER.svg_file(
        storage=storage,
        basename=basename,
        prefix=prefix,
        size=size,
        color=color,
        **kwargs,
    )


def create_inner_bmp_file(
    storage: Optional[BaseStorage] = None,
    basename: Optional[str] = None,
    prefix: Optional[str] = None,
    size: Tuple[int, int] = (100, 100),
    color: Tuple[int, int, int] = (0, 0, 255),
    **kwargs,
) -> StringValue:
    """Create inner BMP file."""
    return FAKER.bmp_file(
        storage=storage,
        basename=basename,
        prefix=prefix,
        size=size,
        color=color,
        **kwargs,
    )


def create_inner_gif_file(
    storage: Optional[BaseStorage] = None,
    basename: Optional[str] = None,
    prefix: Optional[str] = None,
    size: Tuple[int, int] = (100, 100),
    color: Tuple[int, int, int] = (0, 0, 255),
    **kwargs,
) -> StringValue:
    """Create inner GIF file."""
    return FAKER.gif_file(
        storage=storage,
        basename=basename,
        prefix=prefix,
        size=size,
        color=color,
        **kwargs,
    )


def create_inner_tif_file(
    storage: Optional[BaseStorage] = None,
    basename: Optional[str] = None,
    prefix: Optional[str] = None,
    size: Tuple[int, int] = (100, 100),
    color: Tuple[int, int, int] = (0, 0, 255),
    **kwargs,
) -> StringValue:
    """Create inner TIF file."""
    return FAKER.tif_file(
        storage=storage,
        basename=basename,
        prefix=prefix,
        size=size,
        color=color,
        **kwargs,
    )


def create_inner_ppm_file(
    storage: Optional[BaseStorage] = None,
    basename: Optional[str] = None,
    prefix: Optional[str] = None,
    size: Tuple[int, int] = (100, 100),
    color: Tuple[int, int, int] = (0, 0, 255),
    **kwargs,
) -> StringValue:
    """Create inner PPM file."""
    return FAKER.ppm_file(
        storage=storage,
        basename=basename,
        prefix=prefix,
        size=size,
        color=color,
        **kwargs,
    )


def create_inner_wav_file(
    storage: Optional[BaseStorage] = None,
    basename: Optional[str] = None,
    prefix: Optional[str] = None,
    frequency: int = 440,
    duration: int = 1,
    volume: Union[float, int] = 0.5,
    sample_rate: int = 44100,
    **kwargs,
) -> StringValue:
    """Create inner WAV file."""
    return FAKER.wav_file(
        storage=storage,
        basename=basename,
        prefix=prefix,
        frequency=frequency,
        duration=duration,
        volume=volume,
        sample_rate=sample_rate,
        **kwargs,
    )


def create_inner_docx_file(
    storage: Optional[BaseStorage] = None,
    basename: Optional[str] = None,
    prefix: Optional[str] = None,
    nb_pages: Optional[int] = 1,
    texts: Optional[List[str]] = None,
    metadata: Optional[MetaData] = None,
    **kwargs,
) -> StringValue:
    """Create inner DOCX file."""
    return FAKER.docx_file(
        storage=storage,
        basename=basename,
        prefix=prefix,
        nb_pages=nb_pages,
        texts=texts,
        metadata=metadata,
        **kwargs,
    )


def create_inner_odt_file(
    storage: Optional[BaseStorage] = None,
    basename: Optional[str] = None,
    prefix: Optional[str] = None,
    nb_pages: Optional[int] = 1,
    texts: Optional[List[str]] = None,
    metadata: Optional[MetaData] = None,
    **kwargs,
) -> StringValue:
    """Create inner ODT file."""
    return FAKER.odt_file(
        storage=storage,
        basename=basename,
        prefix=prefix,
        nb_pages=nb_pages,
        texts=texts,
        metadata=metadata,
        **kwargs,
    )


def create_inner_zip_file(
    storage: Optional[BaseStorage] = None,
    basename: Optional[str] = None,
    prefix: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    metadata: Optional[MetaData] = None,
    **kwargs,
) -> StringValue:
    """Create inner ZIP file."""
    return FAKER.zip_file(
        storage=storage,
        basename=basename,
        prefix=prefix,
        options=options,
        metadata=metadata,
        **kwargs,
    )


def create_inner_tar_file(
    storage: Optional[BaseStorage] = None,
    basename: Optional[str] = None,
    prefix: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    compression: Optional[Literal["gz", "bz2", "xz"]] = None,
    metadata: Optional[MetaData] = None,
    **kwargs,
) -> StringValue:
    """Create inner TAR file."""
    return FAKER.tar_file(
        storage=storage,
        basename=basename,
        prefix=prefix,
        options=options,
        compression=compression,
        metadata=metadata,
        **kwargs,
    )


def create_inner_eml_file(
    storage: Optional[BaseStorage] = None,
    basename: Optional[str] = None,
    prefix: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    content: Optional[str] = None,
    subject: Optional[str] = None,
    metadata: Optional[MetaData] = None,
    **kwargs,
) -> StringValue:
    """Create inner EML file."""
    return FAKER.eml_file(
        storage=storage,
        basename=basename,
        prefix=prefix,
        options=options,
        content=content,
        subject=subject,
        metadata=metadata,
        **kwargs,
    )


def create_inner_txt_file(
    storage: Optional[BaseStorage] = None,
    basename: Optional[str] = None,
    prefix: Optional[str] = None,
    text: Optional[str] = None,
    **kwargs,
) -> StringValue:
    """Create inner TXT file."""
    if not text:
        text = FAKER.text()

    return FAKER.txt_file(
        storage=storage,
        basename=basename,
        prefix=prefix,
        text=text,
        **kwargs,
    )


def fuzzy_choice_create_inner_file(
    func_choices: List[Tuple[Callable[..., StringValue], Dict[str, Any]]],
    **kwargs,
) -> StringValue:
    """Create inner file from given list of function choices.

    :param func_choices: List of functions to choose from.
    :param **kwargs: Additional keyword arguments to pass to the function.
    :rtype: StringValue
    :return: StringValue instance.

    Usage example:

    .. code-block:: python

        from fake import (
            FAKER,
            FileSystemStorage,
            create_inner_docx_file,
            create_inner_png_file,
            create_inner_txt_file,
            fuzzy_choice_create_inner_file,
        )

        STORAGE = FileSystemStorage()

        kwargs = {"storage": STORAGE}
        file = fuzzy_choice_create_inner_file(
            [
                (create_inner_docx_file, kwargs),
                (create_inner_png_file, kwargs),
                (create_inner_txt_file, kwargs),
            ]
        )

    You could use it in archives to make a variety of different file types
    within the archive.

    .. code-block:: python

        from fake import (
            FAKER,
            FileSystemStorage,
            create_inner_docx_file,
            create_inner_png_file,
            create_inner_txt_file,
            fuzzy_choice_create_inner_file,
        )

        STORAGE = FileSystemStorage()

        kwargs = {"storage": STORAGE}
        file = FAKER.zip_file(
            prefix="zzz_archive_",
            options={
                "count": 50,
                "create_inner_file_func": fuzzy_choice_create_inner_file,
                "create_inner_file_args": {
                    "func_choices": [
                        (create_inner_docx_file, kwargs),
                        (create_inner_png_file, kwargs),
                        (create_inner_txt_file, kwargs),
                    ],
                },
                "directory": "zzz",
            }
        )
    """
    _func, _kwargs = random.choice(func_choices)
    return _func(**_kwargs)


def list_create_inner_file(
    func_list: List[Tuple[Callable[..., StringValue], Dict[str, Any]]],
    **kwargs,
) -> List[StringValue]:
    """Generates multiple files based on the provided list of functions
    and arguments.

    :param func_list: List of tuples, each containing a function to generate a
        file and its arguments.
    :param **kwargs: Additional keyword arguments to pass to the functions.
    :rtype: List[StringValue]
    :return: List of generated file names.

    Usage example:

    .. code-block:: python

        from fake import (
            FAKER,
            FileSystemStorage,
            create_inner_docx_file,
            create_inner_txt_file,
            list_create_inner_file,
        )
        STORAGE = FileSystemStorage()

        kwargs = {"storage": STORAGE, "generator": FAKER}
        file = FAKER.zip_file(
            basename="alice-looking-through-the-glass",
            options={
                "create_inner_file_func": list_create_inner_file,
                "create_inner_file_args": {
                    "func_list": [
                        (create_inner_docx_file, {"basename": "doc"}),
                        (create_inner_txt_file, {"basename": "doc_metadata"}),
                        (create_inner_txt_file, {"basename": "doc_isbn"}),
                    ],
                },
            }
        )

    Note, that while all other inner functions return back `StringValue`
    value, `list_create_inner_file` returns back a `List[StringValue]` value.

    Notably, all inner functions were designed to support archives (such as
    ZIP, TAR and EML, but the list may grow in the future). If the inner
    function passed in the `create_inner_file_func` argument returns a List
    of `StringValue` values, the `option` argument is being ignored and
    generated files are simply limited to what has been passed in
    the `func_list` list of tuples.
    """
    created_files = []
    for func, kwargs in func_list:
        file = func(**kwargs)
        created_files.append(file)
    return created_files


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


def create_factory_method(method_name):
    def method(self, **kwargs):
        return FactoryMethod(method_name, faker=self.faker, **kwargs)

    return method


class SubFactory:
    def __init__(self, factory_class, **kwargs):
        self.factory_class = factory_class
        self.factory_kwargs = kwargs

    def __call__(self):
        # Initialize the specified factory class and create an instance
        return self.factory_class.create(**self.factory_kwargs)


class Factory:
    """Factory."""

    def __init__(self, faker: Optional[Faker] = None) -> None:
        # Directly use the setter to ensure provider methods are added
        self.faker = faker or FAKER

    @property
    def faker(self):
        return self._faker

    @faker.setter
    def faker(self, value):
        self._faker = value
        self._add_provider_methods(value)

    def _add_provider_methods(self, faker_instance):
        for class_name, methods in PROVIDER_REGISTRY.items():
            if (
                class_name == f"{__name__}.{Faker.__name__}"
                or class_name == self.faker.uid
            ):
                for method_name in methods:
                    if hasattr(faker_instance, method_name):
                        bound_method = create_factory_method(method_name)
                        setattr(self, method_name, bound_method.__get__(self))


FACTORY = Factory(faker=FAKER)


def pre_init(func):
    func.is_pre_init = True
    return func


def pre_save(func):
    func.is_pre_save = True
    return func


def post_save(func):
    func.is_post_save = True
    return func


def trait(func):
    func.is_trait = True
    return func


class LazyAttribute:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = self.func(obj)
        setattr(obj, self.func.__name__, value)
        return value


class LazyFunction:
    def __init__(self, func):
        self.func = func

    def __call__(self):
        return self.func()

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.func()


class PreInit:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def execute(self, data: Dict[str, Any]) -> None:
        self.func(data, *self.args, **self.kwargs)


class PreSave:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def execute(self, instance):
        self.func(instance, *self.args, **self.kwargs)


class PostSave:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def execute(self, instance):
        self.func(instance, *self.args, **self.kwargs)


class ModelFactory:
    """ModelFactory."""

    class Meta:
        get_or_create = ("id",)  # Default fields for get_or_create

    def __init_subclass__(cls, **kwargs):
        base_meta = getattr(
            cls.__bases__[0],
            "_meta",
            {
                attr: getattr(cls.__bases__[0].Meta, attr)  # type: ignore
                for attr in dir(cls.__bases__[0].Meta)  # type: ignore
                if not attr.startswith("_")
            },
        )
        cls_meta = {
            attr: getattr(cls.Meta, attr)
            for attr in dir(cls.Meta)
            if not attr.startswith("_")
        }

        cls._meta = {**base_meta, **cls_meta}  # type: ignore

    @classmethod
    def _run_hooks(cls, hooks, instance):
        for method in hooks:
            getattr(cls, method)(cls, instance)

    @classmethod
    def _apply_traits(cls, instance, **kwargs) -> None:
        for name, method in cls.__dict__.items():
            if getattr(method, "is_trait", False) and kwargs.get(name, False):
                method(cls, instance)

    @classmethod
    def _apply_lazy_attributes(cls, instance, model_data):
        for _field, value in model_data.items():
            if isinstance(value, LazyAttribute):
                # Trigger computation and setting of the attribute
                setattr(instance, _field, value.__get__(instance, cls))

    @classmethod
    def create(cls, **kwargs):
        model = cls.Meta.model  # type: ignore
        trait_keys = {
            name
            for name, method in cls.__dict__.items()
            if getattr(method, "is_trait", False)
        }

        # Collect PreInit, PreSave, PostSave methods and prepare model data
        pre_init_methods = {}
        pre_save_methods = {}
        post_save_methods = {}
        model_data = {}
        for _field, value in cls.__dict__.items():
            # Do not process any fields that have been otherwise
            # provided directly using keyword arguments.
            if _field in kwargs:
                continue
            if isinstance(value, PreInit):
                pre_init_methods[_field] = value
            elif isinstance(value, PreSave):
                pre_save_methods[_field] = value
            elif isinstance(value, PostSave):
                post_save_methods[_field] = value
            elif not _field.startswith(
                (
                    "_",
                    "Meta",
                )
            ):
                if (
                    not getattr(value, "is_trait", False)
                    and not getattr(value, "is_pre_init", False)
                    and not getattr(value, "is_pre_save", False)
                    and not getattr(value, "is_post_save", False)
                ):
                    model_data[_field] = (
                        value()
                        if isinstance(
                            value,
                            (FactoryMethod, SubFactory, LazyFunction),
                        )
                        else value
                    )

        # Update model_data with non-trait kwargs and collect PreSave from
        # kwargs.
        for key, value in kwargs.items():
            if isinstance(value, PreInit):
                pre_init_methods[key] = value
            elif isinstance(value, PreSave):
                pre_save_methods[key] = value
            elif isinstance(value, PostSave):
                post_save_methods[key] = value
            elif key not in trait_keys and key not in pre_save_methods:
                model_data[key] = value

        # Execute pre-init methods
        for key, pre_init_method in pre_init_methods.items():
            pre_init_method.execute(model_data)

        # Pre-init hooks
        pre_init_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_pre_init", False)
        ]
        cls._run_hooks(pre_init_hooks, model_data)

        # Create a new instance
        instance = model(**model_data)

        # Apply traits
        cls._apply_traits(instance, **kwargs)

        # Apply LazyAttribute values
        cls._apply_lazy_attributes(instance, model_data)

        # Execute PreSave methods
        for __pre_save_method in pre_save_methods.values():
            __pre_save_method.execute(instance)

        # Pre-save hooks
        pre_save_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_pre_save", False)
        ]
        cls._run_hooks(pre_save_hooks, instance)

        # Save the instance
        cls.save(instance)

        # Execute PostSave methods
        for __post_save_method in post_save_methods.values():
            __post_save_method.execute(instance)

        # Post-save hooks
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


class PydanticModelFactory(ModelFactory):
    """Pydantic ModelFactory."""


class DjangoModelFactory(ModelFactory):
    """Django ModelFactory."""

    @classmethod
    def save(cls, instance):
        instance.save()

    @classmethod
    def create(cls, **kwargs):
        model = cls.Meta.model  # type: ignore
        unique_fields = cls._meta.get("get_or_create", ["id"])  # type: ignore

        trait_keys = {
            name
            for name, method in cls.__dict__.items()
            if getattr(method, "is_trait", False)
        }

        # Construct a query for unique fields
        query = {
            _field: kwargs[_field]
            for _field in unique_fields
            if _field in kwargs
        }

        # Try to get an existing instance
        if query:
            instance = model.objects.filter(**query).first()
            if instance:
                return instance

        # Collect PreInit, PreSave, PostSave methods and prepare model data
        pre_init_methods = {}
        pre_save_methods = {}
        post_save_methods = {}
        model_data = {}
        for _field, value in cls.__dict__.items():
            # Do not process any fields that have been otherwise
            # provided directly using keyword arguments.
            if _field in kwargs:
                continue
            if isinstance(value, PreInit):
                pre_init_methods[_field] = value
            elif isinstance(value, PreSave):
                pre_save_methods[_field] = value
            elif isinstance(value, PostSave):
                post_save_methods[_field] = value
            elif not _field.startswith(
                (
                    "_",
                    "Meta",
                )
            ):
                if (
                    not getattr(value, "is_trait", False)
                    and not getattr(value, "is_pre_init", False)
                    and not getattr(value, "is_pre_save", False)
                    and not getattr(value, "is_post_save", False)
                ):
                    model_data[_field] = (
                        value()
                        if isinstance(
                            value, (FactoryMethod, SubFactory, LazyFunction)
                        )
                        else value
                    )

        # TODO: Check if this block is really needed now, that
        # nested_attrs and direct_attrs are already handled separately
        # later on.
        # Update model_data with non-trait kwargs and collect PreSave
        # from kwargs.
        for key, value in kwargs.items():
            if isinstance(value, PreInit):
                pre_init_methods[key] = value
            elif isinstance(value, PreSave):
                pre_save_methods[key] = value
            elif isinstance(value, PostSave):
                post_save_methods[key] = value

        # Separate nested attributes and direct attributes
        nested_attrs = {k: v for k, v in kwargs.items() if "__" in k}
        direct_attrs = {k: v for k, v in kwargs.items() if "__" not in k}

        # Update direct attributes with callable results
        for _field, value in model_data.items():
            if isinstance(value, (FactoryMethod, SubFactory)):
                model_data[_field] = (
                    value()
                    if _field not in direct_attrs
                    else direct_attrs[_field]
                )

        # Update model_data with non-trait kwargs and collect PreSave
        # and PostSave from direct_attrs.
        for key, value in direct_attrs.items():
            if isinstance(value, PreInit):
                pre_init_methods[key] = value
            elif isinstance(value, PreSave):
                pre_save_methods[key] = value
            elif isinstance(value, PostSave):
                post_save_methods[key] = value
            elif key not in trait_keys and key not in pre_save_methods:
                model_data[key] = value

        # Execute pre-init methods
        for key, pre_init_method in pre_init_methods.items():
            pre_init_method.execute(model_data)

        # Pre-init hooks
        pre_init_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_pre_init", False)
        ]
        cls._run_hooks(pre_init_hooks, model_data)

        # Create a new instance if none found
        instance = model(**model_data)

        # Apply traits
        cls._apply_traits(instance, **kwargs)

        # Apply LazyAttribute values
        cls._apply_lazy_attributes(instance, model_data)

        # Handle nested attributes
        for attr, value in nested_attrs.items():
            field_name, nested_attr = attr.split("__", 1)
            if isinstance(getattr(cls, field_name, None), SubFactory):
                related_instance = getattr(
                    cls, field_name
                ).factory_class.create(**{nested_attr: value})
                setattr(instance, field_name, related_instance)

        # Execute PreSave methods
        for __pre_save_method in pre_save_methods.values():
            __pre_save_method.execute(instance)

        # Run pre-save hooks
        pre_save_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_pre_save", False)
        ]
        cls._run_hooks(pre_save_hooks, instance)

        # Save instance
        cls.save(instance)

        # Execute PostSave methods
        for __post_save_method in post_save_methods.values():
            __post_save_method.execute(instance)

        # Run post-save hooks
        post_save_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_post_save", False)
        ]
        cls._run_hooks(post_save_hooks, instance)

        return instance


def run_async_in_thread(coroutine: Coroutine) -> Awaitable:
    """Run an asynchronous coroutine in a separate thread.

    :param coroutine: An asyncio coroutine to be run.
    :return: The result of the coroutine.
    :rtype: Awaitable
    """

    def thread_target():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coroutine)

    with ThreadPoolExecutor() as executor:
        future = executor.submit(thread_target)
        return future.result()


class TortoiseModelFactory(ModelFactory):
    """Tortoise ModelFactory."""

    @classmethod
    def save(cls, instance):
        async def async_save():
            await instance.save()

        run_async_in_thread(async_save())

    @classmethod
    def create(cls, **kwargs):
        model = cls.Meta.model  # type: ignore
        unique_fields = cls._meta.get("get_or_create", ["id"])  # type: ignore

        trait_keys = {
            name
            for name, method in cls.__dict__.items()
            if getattr(method, "is_trait", False)
        }

        # Construct a query for unique fields
        query = {
            _field: kwargs[_field]
            for _field in unique_fields
            if _field in kwargs
        }

        # Try to get an existing instance
        if query:

            async def async_filter():
                return await model.filter(**query).first()

            instance = run_async_in_thread(async_filter())
            if instance:
                return instance

        # Collect PreInit, PreSave, PostSave methods and prepare model data
        pre_init_methods = {}
        pre_save_methods = {}
        post_save_methods = {}
        model_data = {}
        for _field, value in cls.__dict__.items():
            # Do not process any fields that have been otherwise
            # provided directly using keyword arguments.
            if _field in kwargs:
                continue
            if isinstance(value, PreInit):
                pre_init_methods[_field] = value
            elif isinstance(value, PreSave):
                pre_save_methods[_field] = value
            elif isinstance(value, PostSave):
                post_save_methods[_field] = value
            elif not _field.startswith(
                (
                    "_",
                    "Meta",
                )
            ):
                if (
                    not getattr(value, "is_trait", False)
                    and not getattr(value, "is_pre_init", False)
                    and not getattr(value, "is_pre_save", False)
                    and not getattr(value, "is_post_save", False)
                ):
                    model_data[_field] = (
                        value()
                        if isinstance(
                            value, (FactoryMethod, SubFactory, LazyFunction)
                        )
                        else value
                    )

        # TODO: Check is this block is needed now that kwargs are split
        # into nested_attrs and direct_attrs later on.
        # Update model_data with non-trait kwargs and collect PreSave
        # and PostSave from kwargs.
        for key, value in kwargs.items():
            if isinstance(value, PreSave):
                pre_save_methods[key] = value
            elif isinstance(value, PostSave):
                post_save_methods[key] = value

        # Separate nested attributes and direct attributes
        nested_attrs = {k: v for k, v in kwargs.items() if "__" in k}
        direct_attrs = {k: v for k, v in kwargs.items() if "__" not in k}

        # Update direct attributes with callable results
        for _field, value in model_data.items():
            if isinstance(value, (FactoryMethod, SubFactory)):
                model_data[_field] = (
                    value()
                    if _field not in direct_attrs
                    else direct_attrs[_field]
                )

        # Update model_data with non-trait kwargs and collect PreSave
        # from direct_attrs.
        for key, value in direct_attrs.items():
            if isinstance(value, PreInit):
                pre_init_methods[key] = value
            elif isinstance(value, PreSave):
                pre_save_methods[key] = value
            elif isinstance(value, PostSave):
                post_save_methods[key] = value
            elif key not in trait_keys and key not in pre_save_methods:
                model_data[key] = value

        # Execute pre-init methods
        for key, pre_init_method in pre_init_methods.items():
            pre_init_method.execute(model_data)

        # Pre-init hooks
        pre_init_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_pre_init", False)
        ]
        cls._run_hooks(pre_init_hooks, model_data)

        # Create a new instance if none found
        instance = model(**model_data)

        # Apply traits
        cls._apply_traits(instance, **kwargs)

        # Apply LazyAttribute values
        cls._apply_lazy_attributes(instance, model_data)

        # Handle nested attributes
        for attr, value in nested_attrs.items():
            field_name, nested_attr = attr.split("__", 1)
            if isinstance(getattr(cls, field_name, None), SubFactory):

                async def async_related_instance():
                    return getattr(cls, field_name).factory_class.create(
                        **{nested_attr: value}
                    )

                related_instance = run_async_in_thread(async_related_instance())
                setattr(instance, field_name, related_instance)

        # Execute PreSave methods
        for __pre_save_method in pre_save_methods.values():
            __pre_save_method.execute(instance)

        # Run pre-save hooks
        pre_save_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_pre_save", False)
        ]
        cls._run_hooks(pre_save_hooks, instance)

        # Save instance
        cls.save(instance)

        # Execute PostSave methods
        for __post_save_method in post_save_methods.values():
            __post_save_method.execute(instance)

        # Run post-save hooks
        post_save_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_post_save", False)
        ]
        cls._run_hooks(post_save_hooks, instance)

        return instance


class SQLAlchemyModelFactory(ModelFactory):
    """SQLAlchemy ModelFactory."""

    @classmethod
    def save(cls, instance):
        session = cls.MetaSQLAlchemy.get_session()  # type: ignore
        session.add(instance)
        session.commit()

    @classmethod
    def create(cls, **kwargs):
        session = cls.MetaSQLAlchemy.get_session()  # type: ignore

        model = cls.Meta.model  # type: ignore
        unique_fields = cls._meta.get("get_or_create", ["id"])  # type: ignore

        trait_keys = {
            name
            for name, method in cls.__dict__.items()
            if getattr(method, "is_trait", False)
        }

        # Check for existing instance
        if unique_fields:
            query_kwargs = {
                _field: kwargs.get(_field) for _field in unique_fields
            }
            instance = session.query(model).filter_by(**query_kwargs).first()
            if instance:
                return instance

        # Collect PreInit, PreSave, PostSave methods and prepare model data
        pre_init_methods = {}
        pre_save_methods = {}
        post_save_methods = {}
        model_data = {}
        for _field, value in cls.__dict__.items():
            # Do not process any fields that have been otherwise
            # provided directly using keyword arguments.
            if _field in kwargs:
                continue
            if isinstance(value, PreInit):
                pre_init_methods[_field] = value
            elif isinstance(value, PreSave):
                pre_save_methods[_field] = value
            elif isinstance(value, PostSave):
                post_save_methods[_field] = value
            elif not _field.startswith(
                (
                    "_",
                    "Meta",
                )
            ):
                if (
                    not getattr(value, "is_trait", False)
                    and not getattr(value, "is_pre_init", False)
                    and not getattr(value, "is_pre_save", False)
                    and not getattr(value, "is_post_save", False)
                ):
                    model_data[_field] = (
                        value()
                        if isinstance(
                            value, (FactoryMethod, SubFactory, LazyFunction)
                        )
                        else value
                    )

        # TODO: Check if this is really needed now that kwargs are
        # handled in direct_attrs later on.
        # Update model_data with non-trait kwargs and collect PreSave
        # from kwargs.
        for key, value in kwargs.items():
            if isinstance(value, PreSave):
                pre_save_methods[key] = value
            elif isinstance(value, PostSave):
                post_save_methods[key] = value

        # Separate nested attributes and direct attributes
        nested_attrs = {k: v for k, v in kwargs.items() if "__" in k}
        direct_attrs = {k: v for k, v in kwargs.items() if "__" not in k}

        # Update direct attributes with callable results
        for _field, value in model_data.items():
            if isinstance(value, (FactoryMethod, SubFactory)):
                model_data[_field] = (
                    value()
                    if _field not in direct_attrs
                    else direct_attrs[_field]
                )

        # Update model_data with non-trait kwargs and collect PreSave
        # from direct_attrs.
        for key, value in direct_attrs.items():
            if isinstance(value, PreInit):
                pre_init_methods[key] = value
            elif isinstance(value, PreSave):
                pre_save_methods[key] = value
            elif isinstance(value, PostSave):
                post_save_methods[key] = value
            elif key not in trait_keys and key not in pre_save_methods:
                model_data[key] = value

        # Execute pre-init methods
        for key, pre_init_method in pre_init_methods.items():
            pre_init_method.execute(model_data)

        # Pre-init hooks
        pre_init_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_pre_init", False)
        ]
        cls._run_hooks(pre_init_hooks, model_data)

        # Create a new instance
        instance = model(**model_data)

        # Apply traits
        cls._apply_traits(instance, **kwargs)

        # Apply LazyAttribute values
        cls._apply_lazy_attributes(instance, model_data)

        # Handle nested attributes
        for attr, value in nested_attrs.items():
            field_name, nested_attr = attr.split("__", 1)
            if isinstance(getattr(cls, field_name, None), SubFactory):
                related_instance = getattr(
                    cls, field_name
                ).factory_class.create(**{nested_attr: value})
                setattr(instance, field_name, related_instance)

        # Execute PreSave methods
        for __pre_save_method in pre_save_methods.values():
            __pre_save_method.execute(instance)

        # Run pre-save hooks
        pre_save_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_pre_save", False)
        ]
        cls._run_hooks(pre_save_hooks, instance)

        # Save instance
        cls.save(instance)

        # Execute PostSave methods
        for __post_save_method in post_save_methods.values():
            __post_save_method.execute(instance)

        # Run post-save hooks
        post_save_hooks = [
            method
            for method in dir(cls)
            if getattr(getattr(cls, method), "is_post_save", False)
        ]
        cls._run_hooks(post_save_hooks, instance)

        return instance


# ************************************************
# ******************* Internal *******************
# ************************************************


# TODO: Remove once Python 3.8 support is dropped
class ClassProperty(property):
    """ClassProperty."""

    def __get__(self, cls, owner):
        """Get."""
        return classmethod(self.fget).__get__(None, owner)()  # type: ignore


classproperty = ClassProperty


def xor_transform(val: str, key: int = 10) -> str:
    """Simple, deterministic string encoder/decoder.

    Usage example:

    .. code-block:: python

        val = "abcd"
        encoded_val = xor_transform(val)
        decoded_val = xor_transform(encoded_val)
    """
    return "".join(chr(ord(__c) ^ key) for __c in val)


class BaseDataFiller:
    TYPE_TO_PROVIDER = {
        bool: FAKER.pybool,
        int: FAKER.pyint,
        str: FAKER.pystr,
        datetime: FAKER.date_time,
        date: FAKER.date,
        float: FAKER.pyfloat,
        Decimal: FAKER.pydecimal,
    }

    FIELD_NAME_TO_PROVIDER = {
        "name": FAKER.word,
        "title": FAKER.sentence,
        "slug": FAKER.slug,
        "content": FAKER.text,
        "category": FAKER.word,
        "username": FAKER.username,
        "email": FAKER.email,
        "headline": FAKER.sentence,
        "first_name": FAKER.first_name,
        "last_name": FAKER.last_name,
        "uuid": FAKER.uuid,
        "body": FAKER.text,
        "summary": FAKER.paragraph,
        "date_of_birth": FAKER.date,
        "dob": FAKER.date,
        "age": partial(FAKER.pyint, min_value=1, max_value=100),
        "url": FAKER.url,
    }

    @classmethod
    def get_provider_for_field_name(cls, field_name) -> Optional[Callable]:
        return BaseDataFiller.FIELD_NAME_TO_PROVIDER.get(field_name)


class DataclassDataFiller(BaseDataFiller):
    @classmethod
    def get_provider_for_type(cls, field_type) -> Optional[Callable]:
        """Get provider function for the type given."""
        # Extract the base type from Optional
        if get_origin(field_type) is Optional:
            field_type = get_args(field_type)[0]
        return cls.TYPE_TO_PROVIDER.get(field_type)

    @classmethod
    def fill(cls, dataclass_type: Type) -> Any:
        """Fill dataclass with data."""
        if not is_dataclass(dataclass_type):
            raise ValueError("The provided type must be a dataclass")

        kwargs = {}
        for _field in fields(dataclass_type):
            provider_func = cls.get_provider_for_field_name(_field.name)
            if not provider_func:
                if is_dataclass(_field.type):
                    # Recursive call for nested dataclass
                    def provider_func():
                        return cls.fill(_field.type)

                else:
                    provider_func = cls.get_provider_for_type(_field.type)

            if provider_func:
                kwargs[_field.name] = provider_func()
            else:
                # Skip if no provider function is defined
                continue

        return dataclass_type(**kwargs)


fill_dataclass = DataclassDataFiller.fill


class PydanticDataFiller(BaseDataFiller):
    @classmethod
    def get_provider_for_type(cls, field_type) -> Optional[Callable]:
        if isinstance(field_type, type) and issubclass(
            field_type, (list, dict, set)
        ):
            return None
        if (
            hasattr(field_type, "__origin__")
            and field_type.__origin__ is Optional  # noqa
        ):
            field_type = field_type.__args__[0]  # noqa
        return cls.TYPE_TO_PROVIDER.get(field_type)

    @classmethod
    def is_class_type(cls, type_hint):
        return isinstance(type_hint, type) and not any(
            issubclass(type_hint, primitive)
            for primitive in (int, str, float, bool, Decimal)
        )

    @classmethod
    def fill(cls, object_type: Type) -> Any:
        if not (
            hasattr(object_type, "__fields__")
            and hasattr(object_type, "Config")
        ):
            raise ValueError("The provided type must be a Pydantic model")

        type_hints = get_type_hints(object_type)

        kwargs = {}
        for field_name, field_type in type_hints.items():
            # Check for Pydantic's default_factory
            default_factory = getattr(
                object_type.__fields__[field_name], "default_factory", None
            )
            if default_factory is not None:
                kwargs[field_name] = default_factory()
                continue

            provider_func = cls.get_provider_for_field_name(field_name)

            if not provider_func:
                if cls.is_class_type(field_type):
                    kwargs[field_name] = cls.fill(field_type)
                else:
                    provider_func = cls.get_provider_for_type(field_type)
                    if provider_func:
                        kwargs[field_name] = provider_func()
                    else:
                        continue
            else:
                kwargs[field_name] = provider_func()
        return object_type(**kwargs)


fill_pydantic_model = PydanticDataFiller.fill

# ************************************************
# ********************* CLI **********************
# ************************************************


def get_provider_args(func: Callable) -> Dict[str, Any]:
    """Retrieve the argument list and types for a provider function by
    inspecting its signature.
    """
    sig = signature(func)
    return {param.name: param.annotation for param in sig.parameters.values()}


def get_provider_defaults(func: Callable) -> Dict[str, Any]:
    """Retrieve the argument list and defaults for a provider function by
    inspecting its signature.
    """
    sig = signature(func)
    return {param.name: param.default for param in sig.parameters.values()}


def is_optional_type(type_hint) -> bool:
    """Check if the type hint is an Optional."""
    origin = get_origin(type_hint)
    args = get_args(type_hint)
    return origin is Optional or (origin is Union and type(None) in args)


def get_argparse_type(param_type) -> Any:
    """Get the corresponding argparse type for a given parameter type."""
    origin = get_origin(param_type)
    args = get_args(param_type)
    if origin is Union:
        if type(None) in args:
            non_none_types = [arg for arg in args if arg is not type(None)]
            if len(non_none_types) == 1:
                return get_argparse_type(non_none_types[0])
            return str  # Default to string if multiple types are present
        return str  # Default to string if it's a non-optional Union
    elif origin in [list, tuple, set]:
        return lambda x: [get_argparse_type(args[0])(i) for i in x.split(",")]
    elif param_type is int:
        return int
    elif param_type is float:
        return float
    elif param_type is bool:
        return lambda x: x.lower() in ("true", "1", "yes")
    else:
        return str


def organize_providers(provider_tags) -> Dict[str, Any]:
    """Organize providers by category for easier navigation."""
    categories: Dict[str, Any] = {}
    for _provider, tags in provider_tags:
        for tag in tags:
            if tag not in categories:
                categories[tag] = []
            categories[tag].append(_provider)
    # Sort the providers within each category
    for category in categories:
        categories[category] = sorted(categories[category])

    # Return categories sorted by the category names
    return dict(sorted(categories.items()))


def format_type_hint(type_hint) -> str:
    """Format the type hint for display."""
    origin = get_origin(type_hint)
    _args = get_args(type_hint)
    _type = ", ".join(
        [format_type_hint(arg) for arg in _args if arg is not type(None)]
    )
    if is_optional_type(type_hint):
        return f"Optional[{_type}]"
    elif origin is Tuple:
        formatted_args = []
        for arg in _args:
            if arg is Ellipsis:
                formatted_args.append("...")
            else:
                formatted_args.append(format_type_hint(arg))
        return f"Tuple[{', '.join(formatted_args)}]"
    elif _args:
        return (
            f"{getattr(origin, '__name__', str(origin))}"
            f"[{', '.join([format_type_hint(arg) for arg in _args])}]"
        )
    elif isinstance(type_hint, type) and type_hint.__module__ == "builtins":
        return type_hint.__name__
    elif type_hint is Ellipsis:
        return "..."
    elif isinstance(type_hint, str):
        return type_hint
    else:
        try:
            return f"{type_hint.__module__}.{type_hint.__name__}"
        except Exception:
            return str(type_hint)


class CLI:
    """CLI."""

    def __init__(self, faker: Optional[Faker] = None) -> None:
        if faker:
            self.faker = faker
        else:
            self.faker = FAKER
        faker_id = f"{self.faker.__module__}.{self.faker.__class__.__name__}"
        self.provider_list = sorted(list(PROVIDER_REGISTRY[faker_id]))
        self.provider_tags = [
            (_provider, _provider.tags) for _provider in self.provider_list
        ]
        self.parser = self.setup_parser()
        self.args = self.parser.parse_args()

    def setup_parser(self) -> ArgumentParser:
        _parser = ArgumentParser(
            description=f"CLI for fake.py (version {__version__})",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        subparsers = _parser.add_subparsers(
            dest="command", help="Available commands"
        )

        for provider_name in self.provider_list:
            provider_func = getattr(self.faker, provider_name)
            doc_string = (
                provider_func.__doc__.split("\n")[0]
                if provider_func.__doc__
                else None
            )
            subparser = subparsers.add_parser(provider_name, help=doc_string)
            provider_args = get_provider_args(provider_func)
            provider_defaults = get_provider_defaults(provider_func)
            for param_name, param_type in provider_args.items():
                formatted_type = format_type_hint(param_type)
                default_value = provider_defaults.get(param_name, None)
                argparse_type = get_argparse_type(param_type)
                if is_optional_type(param_type) or default_value is not None:
                    subparser.add_argument(
                        f"--{param_name}",
                        help=f"{param_name} (type: {formatted_type})",
                        type=argparse_type,
                        default=default_value,
                    )
                else:
                    subparser.add_argument(
                        param_name,
                        help=(
                            f"{param_name} (type: {formatted_type}, "
                            f"default value: {default_value})"
                        ),
                        type=argparse_type,
                    )

        return _parser

    def execute_command(self) -> None:
        command = self.args.command
        if not command:
            self.parser.print_help()
            return

        provider_func = getattr(self.faker, command)
        provider_params = signature(provider_func).parameters

        kwargs = {}
        for param_name in provider_params:
            if hasattr(self.args, param_name):
                param_value = getattr(self.args, param_name)
                if param_value is not None:
                    kwargs[param_name] = param_value

        result = provider_func(**kwargs)
        print(result)


def main() -> None:
    cli = CLI()
    cli.execute_command()


if __name__ == "__main__":
    main()

# ************************************************
# ******************** Tests *********************
# ************************************************


class TestScript(unittest.TestCase):
    def test_main(self):
        # Call the script directly and check that it executes without errors
        result = subprocess.run(
            ["python", "fake.py"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        result.stdout.startswith("usage:")


class TestOrganizeProviders(unittest.TestCase):
    def setUp(self):
        self.provider_list = sorted(
            list(PROVIDER_REGISTRY[f"{__name__}.Faker"])
        )
        self.provider_tags = [
            (_provider, _provider.tags) for _provider in self.provider_list
        ]

    def test_organize_providers_empty(self):
        provider_tags: List[Tuple[str, Iterable[str]]] = []
        result = organize_providers(provider_tags)
        expected: Dict[str, Any] = {}
        self.assertEqual(result, expected)

    def test_organize_providers_single_tag(self):
        provider_tags = [(ProviderRegistryItem("provider1"), ("Tag1",))]
        result = organize_providers(provider_tags)
        expected = {"Tag1": [ProviderRegistryItem("provider1")]}
        self.assertEqual(result, expected)

    def test_organize_providers_multiple_tags(self):
        provider_tags = [(ProviderRegistryItem("provider1"), ("Tag1", "Tag2"))]
        result = organize_providers(provider_tags)
        expected = {
            "Tag1": [ProviderRegistryItem("provider1")],
            "Tag2": [ProviderRegistryItem("provider1")],
        }
        self.assertEqual(result, expected)

    def test_organize_providers_multiple_providers(self):
        provider_tags = [
            (ProviderRegistryItem("provider1"), ("Tag1",)),
            (ProviderRegistryItem("provider2"), ("Tag1", "Tag2")),
            (ProviderRegistryItem("provider3"), ("Tag3",)),
        ]
        result = organize_providers(provider_tags)
        expected = {
            "Tag1": [
                ProviderRegistryItem("provider1"),
                ProviderRegistryItem("provider2"),
            ],
            "Tag2": [ProviderRegistryItem("provider2")],
            "Tag3": [ProviderRegistryItem("provider3")],
        }
        self.assertEqual(result, expected)

    def test_organize_providers_sorting(self):
        provider_tags = [
            (ProviderRegistryItem("provider3"), ("Tag1",)),
            (ProviderRegistryItem("provider1"), ("Tag1",)),
            (ProviderRegistryItem("provider2"), ("Tag1",)),
        ]
        result = organize_providers(provider_tags)
        expected = {
            "Tag1": [
                ProviderRegistryItem("provider1"),
                ProviderRegistryItem("provider2"),
                ProviderRegistryItem("provider3"),
            ]
        }
        self.assertEqual(result, expected)

    def test_organize_providers_category_sorting(self):
        provider_tags = [
            (ProviderRegistryItem("provider1"), ("TagB",)),
            (ProviderRegistryItem("provider2"), ("TagA",)),
        ]
        result = organize_providers(provider_tags)
        expected = {
            "TagA": [ProviderRegistryItem("provider2")],
            "TagB": [ProviderRegistryItem("provider1")],
        }
        self.assertEqual(result, expected)


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.provider_list = sorted(
            list(PROVIDER_REGISTRY[f"{__name__}.Faker"])
        )

    @patch("sys.argv", ["fake-py"])
    def test_provider_list(self):
        cli = CLI()
        self.assertEqual(cli.provider_list, self.provider_list)

    @patch("sys.argv", ["fake-py", "pyint"])
    def test_pyint_provider(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            main()
            self.assertTrue(fake_out.getvalue().strip().isdigit())

    @patch(
        "sys.argv",
        [
            "fake-py",
            "generic_file",
            "--content",
            "MyContent",
            "--extension",
            "txt",
            "--basename",
            "my_file",
        ],
    )
    def test_generic_file_provider(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            main()
            self.assertEqual(
                fake_out.getvalue().strip(),
                "tmp/my_file.txt",
            )

    @patch("sys.argv", ["fake-py", "date"])
    def test_date_provider(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            main()
            self.assertRegex(
                fake_out.getvalue().strip(),
                r"\d{4}-\d{2}-\d{2}",
            )

    @patch("sys.argv", ["fake-py", "date", "--start_date=-2d"])
    def test_date_provider_with_args(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            main()
            self.assertRegex(
                fake_out.getvalue().strip(),
                r"\d{4}-\d{2}-\d{2}",
            )

    @patch("sys.argv", ["fake-py", "docx_file", "--nb_pages=1"])
    def test_docx_file_provider(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            main()
            self.assertTrue(fake_out.getvalue().strip().endswith(".docx"))

    @patch("sys.argv", ["fake-py"])
    def test_no_command(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            main()
            self.assertIn(
                "usage: fake-py",
                fake_out.getvalue().strip(),
            )


class TestFaker(unittest.TestCase):
    def setUp(self) -> None:
        self.faker = FAKER

    def tearDown(self):
        FILE_REGISTRY.clean_up()

    @classmethod
    def is_valid_email(cls, email: str) -> bool:
        parsed_address = parseaddr(email)
        return "@" in parsed_address[1]

    def test_uuid(self) -> None:
        uuid_value = self.faker.uuid()
        self.assertIsInstance(uuid_value, uuid.UUID)

    def test_uuids(self) -> None:
        uuids = self.faker.uuids()
        for uuid_value in uuids:
            self.assertIsInstance(uuid_value, uuid.UUID)

    def test_first_name(self) -> None:
        first_name: str = self.faker.first_name()
        self.assertIsInstance(first_name, str)
        self.assertTrue(len(first_name) > 0)
        self.assertIn(first_name, self.faker._first_names)

    def test_first_names(self) -> None:
        first_names: List[str] = self.faker.first_names()
        for first_name in first_names:
            self.assertIsInstance(first_name, str)
            self.assertTrue(len(first_name) > 0)
            self.assertIn(first_name, self.faker._first_names)

    def test_last_name(self) -> None:
        last_name: str = self.faker.last_name()
        self.assertIsInstance(last_name, str)
        self.assertTrue(len(last_name) > 0)
        self.assertIn(last_name, self.faker._last_names)

    def test_last_names(self) -> None:
        last_names: List[str] = self.faker.last_names()
        for last_name in last_names:
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

    def test_names(self) -> None:
        names: List[str] = self.faker.names()
        for name in names:
            self.assertIsInstance(name, str)
            self.assertTrue(len(name) > 0)
            parts = name.split(" ")
            first_name = parts[0]
            last_name = " ".join(parts[1:])
            self.assertIn(first_name, self.faker._first_names)
            self.assertIn(last_name, self.faker._last_names)

    def test_username(self) -> None:
        username: str = self.faker.username()
        self.assertIsInstance(username, str)

    def test_usernames(self) -> None:
        usernames: List[str] = self.faker.usernames()
        for username in usernames:
            self.assertIsInstance(username, str)

    def test_slug(self) -> None:
        slug: str = self.faker.slug()
        self.assertIsInstance(slug, str)

    def test_slugs(self) -> None:
        slugs: List[str] = self.faker.slugs()
        for slug in slugs:
            self.assertIsInstance(slug, str)

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

    def test_file_extension(self) -> None:
        with self.subTest("Return type"):
            _ext = self.faker.file_extension()
            self.assertIsInstance(_ext, str)

        with self.subTest("Extension validity"):
            _ext = self.faker.file_extension()
            self.assertIn(_ext, FILE_EXTENSIONS)

    def test_mime_type(self) -> None:
        with self.subTest("Return type"):
            _mime_type = self.faker.mime_type()
            self.assertIsInstance(_mime_type, str)

        with self.subTest("Mime type validity"):
            _mime_type = self.faker.mime_type()
            self.assertIn(_mime_type, MIME_TYPES)

    def test_tld_with_defaults(self) -> None:
        for _ in range(20):
            result = self.faker.tld()
            self.assertIn(result, TLDS)

    def test_tld_with_custom_tlds(self) -> None:
        custom_tlds = ("edu", "gov", "mil")
        for _ in range(20):
            result = self.faker.tld(custom_tlds)
            self.assertIn(result, custom_tlds)

    def test_domain_name_with_defaults(self) -> None:
        result = self.faker.domain_name()
        parts = result.split(".")
        self.assertEqual(len(parts), 2)
        domain, tld = parts
        self.assertTrue(domain.islower())
        self.assertIn(tld, TLDS)

    def test_domain_name_custom_domain_names(self) -> None:
        custom_tlds = ("edu", "gov", "mil")
        for _ in range(20):
            result = self.faker.domain_name(custom_tlds)
            parts = result.split(".")
            self.assertEqual(len(parts), 2)
            domain, tld = parts
            self.assertTrue(domain.islower())
            self.assertIn(tld, custom_tlds)

    def test_free_email_domain(self):
        for _ in range(20):
            result = self.faker.free_email_domain()
            self.assertIn(result, FREE_EMAIL_DOMAINS)

    def test_email(self) -> None:
        email: str = self.faker.email()
        self.assertIsInstance(email, str)
        self.assertTrue(self.is_valid_email(email))

    def test_email_custom_domain_names(self) -> None:
        domains = [
            ("example.com", "example.com"),
            ("gmail.com", "gmail.com"),
        ]
        for domain, expected_domain in domains:
            with self.subTest(domain=domain, expected_domain=expected_domain):
                kwargs = {"domain_names": [domain]}
                email: str = self.faker.email(**kwargs)
                self.assertIsInstance(email, str)
                self.assertTrue(self.is_valid_email(email))
                self.assertTrue(email.endswith(f"@{expected_domain}"))

    def test_company_email(self) -> None:
        email: str = self.faker.company_email()
        self.assertIsInstance(email, str)
        self.assertTrue(self.is_valid_email(email))

    def test_company_email_custom_domain_names(self) -> None:
        domains = [
            ("microsoft.com", "microsoft.com"),
            ("google.com", "google.com"),
        ]
        for domain, expected_domain in domains:
            with self.subTest(domain=domain, expected_domain=expected_domain):
                kwargs = {"domain_names": [domain]}
                email: str = self.faker.company_email(**kwargs)
                self.assertIsInstance(email, str)
                self.assertTrue(self.is_valid_email(email))
                self.assertTrue(email.endswith(f"@{expected_domain}"))

    def test_free_email(self) -> None:
        email: str = self.faker.free_email()
        self.assertIsInstance(email, str)
        self.assertTrue(self.is_valid_email(email))

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

    def test_image_url(self) -> None:
        params = (
            (None, None, None, {"width": 800, "height": 600}),
            (640, 480, None, {"width": 640, "height": 480}),
            (
                None,
                None,
                "https://example.com/{width}x{height}",
                {"width": 800, "height": 600},
            ),
        )
        for width, height, service_url, expected in params:
            kwargs: Dict[str, Union[str, int, None]] = {}
            if width:
                kwargs["width"] = width
            if height:
                kwargs["height"] = height
            if service_url:
                kwargs["service_url"] = service_url
            image_url = self.faker.image_url(**kwargs)
            self.assertIn(str(expected["width"]), image_url)
            self.assertIn(str(expected["height"]), image_url)
            self.assertTrue(image_url.startswith("https://"))

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

    def test_pydecimal(self):
        with self.subTest("With positive=True"):
            for __ in range(100):
                decimal_number = self.faker.pydecimal(
                    left_digits=3,
                    right_digits=2,
                    positive=True,
                )
                self.assertIsInstance(decimal_number, Decimal)
                self.assertTrue(1 <= decimal_number < 1000)
                # Check if right digits are 2
                self.assertTrue(decimal_number.as_tuple().exponent == -2)

        with self.subTest("With positive=False"):
            for __ in range(100):
                negative_decimal_number = self.faker.pydecimal(
                    left_digits=2,
                    right_digits=2,
                    positive=False,
                )
                self.assertTrue(-100 <= negative_decimal_number <= 100)

        with self.subTest("With right_digits=0"):
            for __ in range(100):
                decimal_number = self.faker.pydecimal(
                    left_digits=2,
                    right_digits=0,
                    positive=True,
                )
                self.assertIsInstance(decimal_number, Decimal)
                # Check if there is no fractional part
                self.assertEqual(decimal_number % 1, 0)
                # Check if it's a 3-digit number
                self.assertTrue(10 <= decimal_number < 100)

        with self.subTest("With left_digits=0"):
            for __ in range(100):
                decimal_number = self.faker.pydecimal(
                    left_digits=0, right_digits=2, positive=True
                )
                self.assertIsInstance(decimal_number, Decimal)
                self.assertTrue(0 <= decimal_number < 1)
                self.assertTrue(
                    10 <= decimal_number * 100 < 100
                )  # Check that the fractional part is correct

                # Test for zero left digits with negative numbers
                decimal_number_neg = self.faker.pydecimal(
                    left_digits=0, right_digits=2, positive=False
                )
                self.assertTrue(-1 < decimal_number_neg <= 0)

        with self.subTest("Fail on `left_digits` < 0"):
            with self.assertRaises(ValueError):
                self.faker.pydecimal(left_digits=-1)

        with self.subTest("Fail on `right_digits` < 0"):
            with self.assertRaises(ValueError):
                self.faker.pydecimal(right_digits=-1)

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
            datetime.now(timezone.utc),
            delta=timedelta(seconds=1),
        )
        self.assertAlmostEqual(
            self.faker._parse_date_string("today"),
            datetime.now(timezone.utc),
            delta=timedelta(seconds=1),
        )

        # Test days, hours, and minutes
        self.assertAlmostEqual(
            self.faker._parse_date_string("1d"),
            datetime.now(timezone.utc) + timedelta(days=1),
            delta=timedelta(seconds=1),
        )
        self.assertAlmostEqual(
            self.faker._parse_date_string("-1H"),
            datetime.now(timezone.utc) - timedelta(hours=1),
            delta=timedelta(seconds=1),
        )
        self.assertAlmostEqual(
            self.faker._parse_date_string("30M"),
            datetime.now(timezone.utc) + timedelta(minutes=30),
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
        self.assertEqual(random_date, datetime.now(timezone.utc).date())

        # Test date range
        start_date = "-2d"
        end_date = "+2d"
        random_date = self.faker.date(start_date, end_date)
        self.assertIsInstance(random_date, date)
        self.assertTrue(
            datetime.now(timezone.utc).date() - timedelta(days=2)
            <= random_date
            <= datetime.now(timezone.utc).date() + timedelta(days=2)
        )

    def test_date_time(self) -> None:
        # Test the same datetime for start and end
        start_date = "now"
        end_date = "+0d"
        random_datetime = self.faker.date_time(start_date, end_date)
        self.assertIsInstance(random_datetime, datetime)
        self.assertAlmostEqual(
            random_datetime,
            datetime.now(timezone.utc),
            delta=timedelta(seconds=1),
        )

        # Test datetime range
        start_date = "-2H"
        end_date = "+2H"
        random_datetime = self.faker.date_time(start_date, end_date)
        self.assertIsInstance(random_datetime, datetime)
        self.assertTrue(
            datetime.now(timezone.utc) - timedelta(hours=2)
            <= random_datetime
            <= datetime.now(timezone.utc) + timedelta(hours=2)
        )

    def test_text_pdf(self) -> None:
        with self.subTest("All params None, should fail"):
            with self.assertRaises(ValueError):
                self.faker.pdf(
                    nb_pages=None,
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

        with self.subTest("With `metadata` provided"):
            metadata = MetaData()
            pdf = self.faker.pdf(
                generator=TextPdfGenerator,
                metadata=metadata,
            )
            self.assertTrue(pdf)
            self.assertIsInstance(pdf, bytes)

        with self.subTest("text_pdf shortcut"):
            metadata = MetaData()
            pdf = self.faker.text_pdf(
                metadata=metadata,
            )
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

    def test_tif(self) -> None:
        tif = self.faker.tif()
        self.assertTrue(tif)
        self.assertIsInstance(tif, bytes)

    def test_ppm(self) -> None:
        ppm = self.faker.ppm()
        self.assertTrue(ppm)
        self.assertIsInstance(ppm, bytes)

    def test_image(self):
        for image_format in {"png", "svg", "bmp", "gif", "tif", "ppm"}:
            with self.subTest(image_format=image_format):
                image = self.faker.image(
                    image_format=image_format,
                )
                self.assertTrue(image)
                self.assertIsInstance(image, bytes)
        for image_format in {"bin"}:
            with self.subTest(image_format=image_format):
                with self.assertRaises(ValueError):
                    self.faker.image(image_format=image_format)

    def test_wav(self) -> None:
        wav = self.faker.wav()
        self.assertTrue(wav)
        self.assertIsInstance(wav, bytes)

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

    def test_odt(self) -> None:
        with self.subTest("All params None, should fail"):
            with self.assertRaises(ValueError):
                self.faker.odt(nb_pages=None, texts=None),  # noqa

        with self.subTest("Without params"):
            odt = self.faker.odt()
            self.assertTrue(odt)
            self.assertIsInstance(odt, bytes)

        with self.subTest("With `texts` provided"):
            texts = self.faker.sentences()
            odt = self.faker.odt(texts=texts)
            self.assertTrue(odt)
            self.assertIsInstance(odt, bytes)

    def test_bin(self) -> None:
        value = self.faker.bin()
        self.assertTrue(value)
        self.assertIsInstance(value, bytes)

    def test_zip(self) -> None:
        value = self.faker.zip()
        self.assertTrue(value)
        self.assertIsInstance(value, bytes)

    def test_tar(self) -> None:
        value = self.faker.tar()
        self.assertTrue(value)
        self.assertIsInstance(value, bytes)

    def test_eml(self) -> None:
        value = self.faker.eml()
        self.assertTrue(value)
        self.assertIsInstance(value, bytes)

    def test_pdf_file(self) -> None:
        file = self.faker.pdf_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_text_pdf_file(self) -> None:
        file = self.faker.text_pdf_file()
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

    def test_tif_file(self) -> None:
        file = self.faker.tif_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_ppm_file(self) -> None:
        file = self.faker.ppm_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_wav_file(self) -> None:
        file = self.faker.wav_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_docx_file(self) -> None:
        file = self.faker.docx_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_odt_file(self) -> None:
        file = self.faker.odt_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_bin_file(self) -> None:
        file = self.faker.bin_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_zip_file(self) -> None:
        file = self.faker.zip_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_tar_file(self) -> None:
        file = self.faker.tar_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_eml_file(self) -> None:
        file = self.faker.eml_file()
        self.assertTrue(os.path.exists(file.data["filename"]))

    def test_txt_file(self) -> None:
        with self.subTest("Without arguments"):
            file = self.faker.txt_file()
            self.assertTrue(os.path.exists(file.data["filename"]))

        with self.subTest("nb_chars=None"):
            file = self.faker.txt_file(nb_chars=None)
            self.assertTrue(os.path.exists(file.data["filename"]))

    def test_generic_file(self) -> None:
        with self.subTest("Without text content"):
            file = self.faker.generic_file(
                content=self.faker.text(),
                extension="txt",
            )
            self.assertTrue(os.path.exists(file.data["filename"]))

        with self.subTest("With bytes content"):
            file = self.faker.generic_file(
                content=self.faker.text().encode(),
                extension="txt",
            )
            self.assertTrue(os.path.exists(file.data["filename"]))

    def test_create_inner_pdf_file(self):
        value = create_inner_pdf_file()
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_text_pdf_file(self):
        value = create_inner_text_pdf_file()
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_png_file(self):
        value = create_inner_png_file()
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_svg_file(self):
        value = create_inner_svg_file()
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_bmp_file(self):
        value = create_inner_bmp_file()
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_gif_file(self):
        value = create_inner_gif_file()
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_tif_file(self):
        value = create_inner_tif_file()
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_ppm_file(self):
        value = create_inner_ppm_file()
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_wav_file(self):
        value = create_inner_wav_file()
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_docx_file(self):
        value = create_inner_docx_file()
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_odt_file(self):
        value = create_inner_odt_file()
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_zip_file(self):
        value = create_inner_zip_file()
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_zip_file_with_options(self):
        value = create_inner_zip_file(
            prefix="zzz_archive_",
            options={
                "count": 5,
                "create_inner_file_func": create_inner_txt_file,
                "create_inner_file_args": {
                    "prefix": "zzz_file_",
                },
                "directory": "zzz",
            },
        )
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_zip_file_with_options_list_create(self):
        value = create_inner_zip_file(
            basename="alice-looking-through-the-glass",
            options={
                "create_inner_file_func": list_create_inner_file,
                "create_inner_file_args": {
                    "func_list": [
                        (create_inner_txt_file, {}),
                        (create_inner_txt_file, {}),
                        (create_inner_docx_file, {}),
                    ]
                },
            },
        )
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_tar_file(self):
        value = create_inner_tar_file()
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_tar_file_with_options(self):
        value = create_inner_tar_file(
            prefix="ttt_archive_",
            options={
                "count": 5,
                "create_inner_file_func": create_inner_txt_file,
                "create_inner_file_args": {
                    "prefix": "ttt_file_",
                },
                "directory": "ttt",
            },
        )
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_tar_file_with_options_list_create(self):
        value = create_inner_tar_file(
            basename="alice-looking-through-the-glass",
            options={
                "create_inner_file_func": list_create_inner_file,
                "create_inner_file_args": {
                    "func_list": [
                        (create_inner_txt_file, {}),
                        (create_inner_txt_file, {}),
                        (create_inner_docx_file, {}),
                    ]
                },
            },
        )
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_eml_file(self):
        value = create_inner_eml_file()
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_eml_file_with_options(self):
        value = create_inner_eml_file(
            prefix="eee_email_",
            options={
                "count": 5,
                "create_inner_file_func": create_inner_docx_file,
                "create_inner_file_args": {
                    "prefix": "eee_file_",
                },
            },
        )
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_eml_file_with_options_list_create(self):
        value = create_inner_eml_file(
            basename="alice-looking-through-the-glass",
            options={
                "create_inner_file_func": list_create_inner_file,
                "create_inner_file_args": {
                    "func_list": [
                        (create_inner_txt_file, {}),
                        (create_inner_txt_file, {}),
                        (create_inner_docx_file, {}),
                    ]
                },
            },
        )
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_create_inner_txt_file(self):
        value = create_inner_txt_file()
        self.assertTrue(value)
        self.assertIsInstance(value, StringValue)

    def test_random_choice(self) -> None:
        _categories = ["art", "technology", "literature"]
        _choice = self.faker.random_choice(_categories)
        self.assertIn(_choice, _categories)

    def test_random_sample(self) -> None:
        _categories = ["art", "technology", "literature"]
        _sample = self.faker.random_sample(_categories, 2)
        self.assertEqual(len(_sample), 2)
        for _element in _sample:
            self.assertIn(_element, _categories)

    def test_city(self):
        city = self.faker.city()
        self.assertIn(city, self.faker._cities)

    def test_country(self):
        country = self.faker.country()
        self.assertIn(country, self.faker._countries)

    def test_geo_location(self):
        geo_location = self.faker.geo_location()
        self.assertIn(geo_location, self.faker._geo_locations)

    def test_country_code(self):
        country_code = self.faker.country_code()
        self.assertIn(country_code, self.faker._country_codes)
        self.assertTrue(len(country_code) == 2)
        self.assertTrue(country_code.isupper())

    def test_locale(self):
        _locale = self.faker.locale()
        self.assertIn(_locale, self.faker._locales)
        self.assertIn("_", _locale)
        parts = _locale.split("_")
        self.assertTrue(len(parts), 2)

    def test_latitude(self):
        """Test that the latitude function returns a valid latitude."""
        for _ in range(50):  # Run multiple times to test randomness
            lat = self.faker.latitude()
            self.assertTrue(-90 <= lat <= 90)

    def test_longitude(self):
        """Test that the longitude function returns a valid longitude."""
        for _ in range(50):  # Run multiple times to test randomness
            lon = self.faker.longitude()
            self.assertTrue(-180 <= lon <= 180)

    def test_latitude_longitude(self):
        """Test that the latlng returns a valid (latitude, longitude) pair."""
        for _ in range(50):  # Run multiple times to test randomness
            lat, lon = self.faker.latitude_longitude()
            self.assertTrue(-90 <= lat <= 90)
            self.assertTrue(-180 <= lon <= 180)

    def test_iban(self):
        iban = self.faker.iban()
        self.assertEqual(len(iban), 22)
        self.assertTrue(iban[:2].isalpha())
        self.assertTrue(iban[2:4].isdigit())
        self.assertTrue(iban[4:].isdigit())

    def test_isbn10(self):
        isbn10 = self.faker.isbn10()
        self.assertTrue(isbn10.count("-"), 3)
        parts = isbn10.split("-")
        self.assertEqual(len(parts), 4)
        self.assertTrue(all(part.isdigit() for part in parts[:-1]))
        self.assertTrue(parts[-1].isdigit() or parts[-1] == "X")

    def test_isbn13(self):
        isbn13 = self.faker.isbn13()
        self.assertTrue(isbn13.count("-"), 4)
        parts = isbn13.split("-")
        self.assertEqual(len(parts), 5)
        self.assertTrue(parts[0] in ["978", "979"])
        self.assertTrue(all(part.isdigit() for part in parts[1:]))

    def test_isbn13_checksum(self):
        # Generate an ISBN-13 excluding the checksum
        prefix = random.choice(["978", "979"])
        digits = [str(random.randint(0, 9)) for _ in range(9)]
        full_digits = list(prefix) + digits
        # Get the checksum using the _isbn13_checksum method
        calculated_checksum = self.faker._isbn13_checksum(full_digits)
        # Append the checksum and form the full ISBN-13
        isbn = "".join(full_digits) + calculated_checksum
        # Re-calculate to verify correctness
        self.assertEqual(
            calculated_checksum,
            self.faker._isbn13_checksum(list(isbn[:-1])),
        )

    def test_randomise_string(self):
        # Test pattern with both letters and digits placeholders
        pattern = "??##-####-??"
        expected_length = len(pattern)
        result = self.faker.randomise_string(pattern)

        self.assertEqual(len(result), expected_length)
        self.assertTrue(
            all(char in string.ascii_uppercase for char in result[:2])
        )
        self.assertTrue(all(char in string.digits for char in result[2:4]))
        self.assertEqual(
            result[4],
            "-",
        )
        self.assertTrue(all(char in string.digits for char in result[5:9]))
        self.assertEqual(result[9], "-")
        self.assertTrue(
            all(char in string.ascii_uppercase for char in result[10:])
        )

        # Test pattern with only letters placeholders
        pattern = "???"
        result = self.faker.randomise_string(pattern)
        self.assertEqual(len(result), len(pattern))
        self.assertTrue(all(char in string.ascii_uppercase for char in result))

        # Test pattern with only digits placeholders
        pattern = "###"
        result = self.faker.randomise_string(pattern)
        self.assertEqual(len(result), len(pattern))
        self.assertTrue(all(char in string.digits for char in result))

        # Test pattern with no placeholders
        pattern = "ABC-123"
        result = self.faker.randomise_string(pattern)
        self.assertEqual(result, pattern)

    def test_storage(self) -> None:
        storage = FileSystemStorage()
        with self.assertRaises(Exception):
            storage.generate_filename(extension=None)  # type: ignore

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

        with self.subTest("Test storage.abspath using relative path"):
            self.assertEqual(
                os.path.realpath(storage.abspath(str(file))),
                os.path.realpath(file.data["filename"]),
            )
        with self.subTest("Test storage.abspath using absolute path"):
            self.assertEqual(
                os.path.realpath(storage.abspath(file.data["filename"])),
                os.path.realpath(file.data["filename"]),
            )

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

    def test_authorship_data(self):
        """Test `AuthorshipData`."""
        authorship_data = AuthorshipData()
        with self.subTest("Testing UnicodeDecodeError case"):
            # Creating a text file with non-UTF-8 characters.
            # Using a character that is not compatible with UTF-8 but is with
            # Latin-1. For example, the byte sequence for a character not
            # representable in UTF-8.
            file = self.faker.generic_file(
                content=b"\xff\xff",
                extension="txt",
                basename="non_utf8_file",
            )
            val = authorship_data._find_authorship_info(file.data["filename"])
            self.assertFalse(val)

    def test_metadata(self) -> None:
        """Test MetaData."""
        with self.subTest("Test str"):
            metadata = MetaData()
            content = self.faker.word()
            metadata.add_content(content)
            self.assertEqual(metadata.content, content)
        with self.subTest("Test list"):
            metadata = MetaData()
            content = self.faker.words()
            metadata.add_content(content)
            self.assertEqual(metadata.content, "\n".join(content))

    def test_faker_init(self) -> None:
        faker = Faker(alias="default")
        self.assertNotEqual(faker.alias, "default")

    def test_get_by_uid(self) -> None:
        faker = Faker.get_by_uid(f"{__name__}.{Faker.__name__}")
        self.assertIs(faker, self.faker)

    def test_get_by_alias(self) -> None:
        faker = Faker.get_by_alias("default")
        self.assertIs(faker, self.faker)

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

    def test_factory_methods(self) -> None:
        # Assuming 'Faker' is the class with methods decorated by @provider
        faker = Faker()
        factory = Factory(faker)

        # Iterate through methods of Faker
        for attr_name in dir(faker):
            attr_value = getattr(faker, attr_name)
            if callable(attr_value) and getattr(
                attr_value, "is_provider", False
            ):
                # Check if Factory has the method
                self.assertTrue(hasattr(factory, attr_name))

    def test_sub_factory(self) -> None:
        """Test FACTORY and SubFactory."""

        # *************************
        # ********* Models ********
        # *************************

        class MockPydanticField:
            """Mock field simulating a Pydantic model field."""

            def __init__(self, type, default_factory):
                self.type = type
                self.default_factory = default_factory

        class MockPydanticModel:
            """Mock class simulating a Pydantic model."""

            # Adjusting __fields__ to mimic Pydantic's structure
            __fields__ = {
                "id": MockPydanticField(int, lambda: 1),
                "name": MockPydanticField(str, lambda: "default"),
                "is_active": MockPydanticField(bool, lambda: True),
                "created_at": MockPydanticField(datetime, datetime.now),
                "optional_field": MockPydanticField(
                    Optional[str], lambda: None
                ),
            }

            class Config:
                arbitrary_types_allowed = True

            id: int
            name: str
            is_active: bool
            created_at: datetime
            optional_field: Optional[str] = None

            def __init__(self, **kwargs):
                for name, value in kwargs.items():
                    setattr(self, name, value)

        class DjangoQuerySet(list):
            """Mimicking Django QuerySet class."""

            def __init__(self, instance: Union["Article", "User"]) -> None:
                super().__init__()
                self.instance = instance

            def first(self) -> Union["Article", "User"]:
                return self.instance

        class DjangoManager:
            """Mimicking Django Manager class."""

            def __init__(self, instance: Union["Article", "User"]) -> None:
                self.instance = instance

            def filter(self, *args, **kwargs) -> "DjangoQuerySet":
                return DjangoQuerySet(instance=self.instance)

        @dataclass(frozen=True)
        class Group:
            id: int
            name: str

        @dataclass
        class User:
            """User model."""

            id: int
            username: str
            first_name: str
            last_name: str
            email: str
            date_joined: datetime = field(default_factory=datetime.utcnow)
            last_login: Optional[datetime] = None
            password: Optional[str] = None
            is_superuser: bool = False
            is_staff: bool = False
            is_active: bool = True
            groups: Set[Group] = field(default_factory=set)

            def save(self, *args, **kwargs):
                """Mimicking Django's Mode save method."""
                self.save_called = True  # noqa

            def set_password(self, password: str) -> None:
                self.password = xor_transform(password)

            # TODO: Remove once Python 3.8 support is dropped
            #  and replace with @classmethod @property combo.
            @classproperty
            def objects(cls):
                """Mimicking Django's Manager behaviour."""
                return DjangoManager(
                    instance=fill_dataclass(cls),  # type: ignore
                )

        @dataclass
        class Article:
            id: int
            title: str
            slug: str
            content: str
            headline: str
            category: str
            pages: int
            auto_minutes_to_read: int
            author: User
            image: Optional[str] = (
                None  # Use str to represent the image path or URL
            )
            pub_date: date = field(default_factory=date.today)
            safe_for_work: bool = False
            minutes_to_read: int = 5

            def save(self, *args, **kwargs):
                """Mimicking Django's Mode save method."""
                self.save_called = True  # noqa

            # TODO: Remove once Python 3.8 support is dropped
            #  and replace with @classmethod @property combo.
            @classproperty
            def objects(cls):
                """Mimicking Django's Manager behaviour."""
                return DjangoManager(
                    instance=fill_dataclass(cls),  # type: ignore
                )

        with self.subTest("fill_pydantic_model on dataclass"):
            with self.assertRaises(ValueError):
                _article = fill_pydantic_model(Article)

        with self.subTest("fill_pydantic_model"):
            _obj = fill_pydantic_model(MockPydanticModel)

        with self.subTest("fill_dataclass"):
            _article = fill_dataclass(Article)

        # ****************************
        # *********** Other **********
        # ****************************

        base_dir = Path(__file__).resolve().parent.parent
        media_root = base_dir / "media"

        storage = FileSystemStorage(root_path=media_root, rel_path="tmp")

        # ****************************
        # ******* ModelFactory *******
        # ****************************

        def set_password(user: Any, password: str) -> None:
            user.set_password(password)

        def add_to_group(user: Any, name: str) -> None:
            group = GroupFactory(name=name)
            user.groups.add(group)

        categories = (
            "art",
            "technology",
            "literature",
        )

        class GroupFactory(ModelFactory):
            id = FACTORY.pyint()  # type: ignore
            name = FACTORY.word()  # type: ignore

            class Meta:
                model = Group
                get_or_create = ("name",)

        class UserFactory(ModelFactory):
            id = FACTORY.pyint()  # type: ignore
            username = FACTORY.username()  # type: ignore
            first_name = FACTORY.first_name()  # type: ignore
            last_name = FACTORY.last_name()  # type: ignore
            email = FACTORY.email()  # type: ignore
            last_login = FACTORY.date_time()  # type: ignore
            is_superuser = False
            is_staff = False
            is_active = FACTORY.pybool()  # type: ignore
            date_joined = FACTORY.date_time()  # type: ignore
            password = PreSave(set_password, password="test1234")
            group = PostSave(add_to_group, name="TestGroup1234")

            class Meta:
                model = User

            @trait
            def is_admin_user(self, instance: User) -> None:
                instance.is_superuser = True
                instance.is_staff = True
                instance.is_active = True

            @pre_save
            def _pre_save_method(self, instance):
                instance._pre_save_called = True

            @post_save
            def _post_save_method(self, instance):
                instance._post_save_called = True

        def set_auto_minutes_to_read(data):
            data["auto_minutes_to_read"] = data["pages"]

        class ArticleFactory(ModelFactory):
            id = FACTORY.pyint()  # type: ignore
            title = FACTORY.sentence()  # type: ignore
            slug = FACTORY.slug()  # type: ignore
            content = FACTORY.text()  # type: ignore
            headline = LazyAttribute(lambda o: o.content[:25])
            category = LazyFunction(partial(random.choice, categories))
            pages = FACTORY.pyint(min_value=1, max_value=100)  # type: ignore
            auto_minutes_to_read = PreInit(set_auto_minutes_to_read)
            image = FACTORY.png_file(storage=storage)  # type: ignore
            pub_date = FACTORY.date()  # type: ignore
            safe_for_work = FACTORY.pybool()  # type: ignore
            minutes_to_read = FACTORY.pyint(  # type: ignore
                min_value=1, max_value=10
            )
            author = SubFactory(UserFactory)

            class Meta:
                model = Article

        with self.subTest("ModelFactory"):
            _article = ArticleFactory()

            # Testing SubFactory
            self.assertIsInstance(_article.author, User)
            self.assertIsInstance(_article.author.id, int)
            self.assertIsInstance(
                _article.author.is_staff,
                bool,
            )
            self.assertIsInstance(
                _article.author.date_joined,
                datetime,
            )

            # Testing LazyFunction
            self.assertIn(_article.category, categories)

            # Testing LazyAttribute
            self.assertIn(_article.headline, _article.content)

            # Testing PreInit
            self.assertEqual(_article.pages, _article.auto_minutes_to_read)

            # Testing Factory
            self.assertIsInstance(_article.id, int)
            self.assertIsInstance(_article.slug, str)

            # Testing hooks
            _user = _article.author
            self.assertTrue(
                hasattr(_user, "_pre_save_called") and _user._pre_save_called
            )
            self.assertTrue(
                hasattr(_user, "_post_save_called") and _user._post_save_called
            )

            # Testing get_or_create for Article model
            _article = ArticleFactory(id=1)
            self.assertIsInstance(_article, Article)
            self.assertEqual(_article.id, 1)

            # Testing traits
            _admin_user = UserFactory(is_admin_user=True)
            self.assertTrue(
                _admin_user.is_staff
                and _admin_user.is_superuser
                and _admin_user.is_active
            )

            # Testing PreSave
            self.assertEqual(xor_transform(str(_user.password)), "test1234")
            _user = UserFactory(
                password=PreSave(set_password, password="1234test")
            )
            self.assertEqual(xor_transform(str(_user.password)), "1234test")

            # Testing PostSave
            self.assertEqual(list(_user.groups)[0].name, "TestGroup1234")
            _user = UserFactory(
                group=PostSave(add_to_group, name="1234TestGroup")
            )
            self.assertEqual(list(_user.groups)[0].name, "1234TestGroup")

        # **********************************
        # ******* DjangoModelFactory *******
        # **********************************

        class DjangoUserFactory(DjangoModelFactory):
            id = FACTORY.pyint()  # type: ignore
            username = FACTORY.username()  # type: ignore
            first_name = FACTORY.first_name()  # type: ignore
            last_name = FACTORY.last_name()  # type: ignore
            email = FACTORY.email()  # type: ignore
            last_login = FACTORY.date_time()  # type: ignore
            is_superuser = False
            is_staff = False
            is_active = FACTORY.pybool()  # type: ignore
            date_joined = FACTORY.date_time()  # type: ignore
            password = PreSave(set_password, password="jest1234")
            group = PostSave(add_to_group, name="JestGroup1234")

            class Meta:
                model = User
                get_or_create = ("username",)

            @trait
            def is_admin_user(self, instance: User) -> None:
                instance.is_superuser = True
                instance.is_staff = True
                instance.is_active = True

            @pre_save
            def _pre_save_method(self, instance):
                instance._pre_save_called = True

            @post_save
            def _post_save_method(self, instance):
                instance._post_save_called = True

        class DjangoArticleFactory(DjangoModelFactory):
            id = FACTORY.pyint()  # type: ignore
            title = FACTORY.sentence()  # type: ignore
            slug = FACTORY.slug()  # type: ignore
            content = FACTORY.text()  # type: ignore
            headline = LazyAttribute(lambda o: o.content[:25])
            category = LazyFunction(partial(random.choice, categories))
            pages = FACTORY.pyint(min_value=1, max_value=100)  # type: ignore
            auto_minutes_to_read = PreInit(set_auto_minutes_to_read)
            image = FACTORY.png_file(storage=storage)  # type: ignore
            pub_date = FACTORY.date()  # type: ignore
            safe_for_work = FACTORY.pybool()  # type: ignore
            minutes_to_read = FACTORY.pyint(  # type: ignore
                min_value=1,
                max_value=10,
            )
            author = SubFactory(DjangoUserFactory)

            class Meta:
                model = Article

            @pre_save
            def _pre_save_method(self, instance):
                instance._pre_save_called = True

            @post_save
            def _post_save_method(self, instance):
                instance._post_save_called = True

        with self.subTest("DjangoModelFactory"):
            _django_article = DjangoArticleFactory(author__username="admin")

            # Testing SubFactory
            self.assertIsInstance(_django_article.author, User)
            self.assertIsInstance(
                _django_article.author.id,  # type: ignore
                int,
            )
            self.assertIsInstance(
                _django_article.author.is_staff,  # type: ignore
                bool,
            )
            self.assertIsInstance(
                _django_article.author.date_joined,  # type: ignore
                datetime,
            )
            # Since we're mimicking Django's behaviour, the following line would
            # fail on test, however would pass when testing against real Django
            # model (as done in the examples).
            # self.assertEqual(django_article.author.username, "admin")

            # Testing Factory
            self.assertIsInstance(_django_article.id, int)
            self.assertIsInstance(_django_article.slug, str)

            # Testing PreInit
            self.assertEqual(
                _django_article.pages,
                _django_article.auto_minutes_to_read,
            )

            # Testing hooks
            self.assertTrue(
                hasattr(_django_article, "_pre_save_called")
                and _django_article._pre_save_called
            )
            self.assertTrue(
                hasattr(_django_article, "_post_save_called")
                and _django_article._post_save_called
            )

            # Testing batch creation
            _django_articles = DjangoArticleFactory.create_batch(5)
            self.assertEqual(len(_django_articles), 5)
            self.assertIsInstance(_django_articles[0], Article)

            # Testing get_or_create for Article model
            _django_article = DjangoArticleFactory(id=1)
            self.assertIsInstance(_django_article, Article)

            # Testing traits
            _django_admin_user = DjangoUserFactory(is_admin_user=True)
            self.assertTrue(
                _django_admin_user.is_staff
                and _django_admin_user.is_superuser
                and _django_admin_user.is_active
            )

            # Testing PreSave
            _django_user = DjangoUserFactory()
            self.assertEqual(
                xor_transform(str(_django_user.password)),
                "jest1234",
            )
            _django_user = DjangoUserFactory(
                password=PreSave(set_password, password="1234jest")
            )
            self.assertEqual(
                xor_transform(str(_django_user.password)),
                "1234jest",
            )

            # Testing PostSave
            self.assertEqual(
                list(_django_user.groups)[0].name,  # type: ignore
                "JestGroup1234",
            )
            _django_user = DjangoUserFactory(
                group=PostSave(add_to_group, name="1234JestGroup")
            )
            self.assertEqual(
                list(_django_user.groups)[0].name,  # type: ignore
                "1234JestGroup",
            )

        # **********************************
        # ****** TortoiseModelFactory ******
        # **********************************

        class TortoiseQuerySet(list):
            """Mimicking Tortoise QuerySet class."""

            return_instance_on_query_first: bool = False

            def __init__(
                self,
                instance: Union["TortoiseArticle", "TortoiseUser"],
            ) -> None:
                super().__init__()
                self.instance = instance

            async def first(
                self,
            ) -> Optional[Union["TortoiseArticle", "TortoiseUser"]]:
                if not self.return_instance_on_query_first:
                    return None
                return self.instance

        @dataclass(frozen=True)
        class TortoiseGroup:
            id: int
            name: str

            @classmethod
            def filter(cls, *args, **kwargs) -> "TortoiseQuerySet":
                return TortoiseQuerySet(instance=fill_dataclass(cls))

            async def save(self, *args, **kwargs):
                """Mimicking Django's Mode save method."""

        @dataclass
        class TortoiseUser:
            """User model."""

            id: int
            username: str
            first_name: str
            last_name: str
            email: str
            date_joined: datetime = field(default_factory=datetime.utcnow)
            last_login: Optional[datetime] = None
            password: Optional[str] = None
            is_superuser: bool = False
            is_staff: bool = False
            is_active: bool = True
            groups: Set[TortoiseGroup] = field(default_factory=set)

            def set_password(self, password: str) -> None:
                self.password = xor_transform(password)

            @classmethod
            def filter(cls, *args, **kwargs) -> "TortoiseQuerySet":
                return TortoiseQuerySet(instance=fill_dataclass(cls))

            async def save(self, *args, **kwargs):
                """Mimicking Django's Mode save method."""
                self.save_called = True  # noqa

        @dataclass
        class TortoiseArticle:
            id: int
            title: str
            slug: str
            content: str
            headline: str
            category: str
            pages: int
            auto_minutes_to_read: int
            author: TortoiseUser
            image: Optional[str] = (
                None  # Use str to represent the image path or URL
            )
            pub_date: date = field(default_factory=date.today)
            safe_for_work: bool = False
            minutes_to_read: int = 5

            @classmethod
            def filter(cls, *args, **kwargs) -> "TortoiseQuerySet":
                return TortoiseQuerySet(instance=fill_dataclass(cls))

            async def save(self, *args, **kwargs):
                """Mimicking Django's Mode save method."""
                self.save_called = True  # noqa

        def add_to_tortoise_group(user: Any, name: str) -> None:
            group = TortoiseGroupFactory(name=name)
            user.groups.add(group)

        class TortoiseGroupFactory(TortoiseModelFactory):
            id = FACTORY.pyint()  # type: ignore
            name = FACTORY.word()  # type: ignore

            class Meta:
                model = TortoiseGroup
                get_or_create = ("name",)

        class TortoiseUserFactory(TortoiseModelFactory):
            id = FACTORY.pyint()  # type: ignore
            username = FACTORY.username()  # type: ignore
            first_name = FACTORY.first_name()  # type: ignore
            last_name = FACTORY.last_name()  # type: ignore
            email = FACTORY.email()  # type: ignore
            last_login = FACTORY.date_time()  # type: ignore
            is_superuser = False
            is_staff = False
            is_active = FACTORY.pybool()  # type: ignore
            date_joined = FACTORY.date_time()  # type: ignore
            password = PreSave(set_password, password="tost1234")
            group = PostSave(add_to_tortoise_group, name="TostGroup1234")

            class Meta:
                model = TortoiseUser
                get_or_create = ("username",)

            @trait
            def is_admin_user(self, instance: TortoiseUser) -> None:
                instance.is_superuser = True
                instance.is_staff = True
                instance.is_active = True

            @pre_save
            def _pre_save_method(self, instance):
                instance._pre_save_called = True

            @post_save
            def _post_save_method(self, instance):
                instance._post_save_called = True

        class TortoiseArticleFactory(TortoiseModelFactory):
            id = FACTORY.pyint()  # type: ignore
            title = FACTORY.sentence()  # type: ignore
            slug = FACTORY.slug()  # type: ignore
            content = FACTORY.text()  # type: ignore
            headline = LazyAttribute(lambda o: o.content[:25])
            category = LazyFunction(partial(random.choice, categories))
            pages = FACTORY.pyint(min_value=1, max_value=100)  # type: ignore
            auto_minutes_to_read = PreInit(set_auto_minutes_to_read)
            image = FACTORY.png_file(storage=storage)  # type: ignore
            pub_date = FACTORY.date()  # type: ignore
            safe_for_work = FACTORY.pybool()  # type: ignore
            minutes_to_read = FACTORY.pyint(  # type: ignore
                min_value=1,
                max_value=10,
            )
            author = SubFactory(TortoiseUserFactory)

            class Meta:
                model = TortoiseArticle

            @pre_save
            def _pre_save_method(self, instance):
                instance._pre_save_called = True

            @post_save
            def _post_save_method(self, instance):
                instance._post_save_called = True

        with self.subTest("TortoiseModelFactory"):
            _tortoise_article = TortoiseArticleFactory(author__username="admin")

            # Testing SubFactory
            self.assertIsInstance(_tortoise_article.author, TortoiseUser)
            self.assertIsInstance(
                _tortoise_article.author.id,  # type: ignore
                int,
            )
            self.assertIsInstance(
                _tortoise_article.author.is_staff,  # type: ignore
                bool,
            )
            self.assertIsInstance(
                _tortoise_article.author.date_joined,  # type: ignore
                datetime,
            )
            # Since we're mimicking Tortoise's behaviour, the following line
            # would fail on test, however would pass when testing against
            # real Tortoise model (as done in the examples).
            # self.assertEqual(tortoise_article.author.username, "admin")

            # Testing Factory
            self.assertIsInstance(_tortoise_article.id, int)
            self.assertIsInstance(_tortoise_article.slug, str)

            # Testing PreInit
            self.assertEqual(
                _tortoise_article.pages,
                _tortoise_article.auto_minutes_to_read,
            )

            # Testing hooks
            self.assertTrue(
                hasattr(_tortoise_article, "_pre_save_called")
                and _tortoise_article._pre_save_called
            )
            self.assertTrue(
                hasattr(_tortoise_article, "_post_save_called")
                and _tortoise_article._post_save_called
            )

            # Testing batch creation
            _tortoise_articles = TortoiseArticleFactory.create_batch(5)
            self.assertEqual(len(_tortoise_articles), 5)
            self.assertIsInstance(_tortoise_articles[0], TortoiseArticle)

            # Testing get_or_create for Article model
            _tortoise_article = TortoiseArticleFactory(id=1)
            self.assertIsInstance(_tortoise_article, TortoiseArticle)

            # Testing traits
            _tortoise_admin_user = TortoiseUserFactory(is_admin_user=True)
            self.assertTrue(
                _tortoise_admin_user.is_staff
                and _tortoise_admin_user.is_superuser
                and _tortoise_admin_user.is_active
            )

            # Testing PreSave
            _tortoise_user = TortoiseUserFactory()
            self.assertEqual(
                xor_transform(str(_tortoise_user.password)),
                "tost1234",
            )
            _tortoise_user = TortoiseUserFactory(
                password=PreSave(set_password, password="1234tost")
            )
            self.assertEqual(
                xor_transform(str(_tortoise_user.password)),
                "1234tost",
            )

            # Testing PostSave
            self.assertEqual(
                list(_tortoise_user.groups)[0].name,  # type: ignore
                "TostGroup1234",
            )
            _tortoise_user = TortoiseUserFactory(
                group=PostSave(add_to_tortoise_group, name="1234TostGroup")
            )
            self.assertEqual(
                list(_tortoise_user.groups)[0].name,  # type: ignore
                "1234TostGroup",
            )

            # **********************************
            # ** Repeat for another condition **
            TortoiseQuerySet.return_instance_on_query_first = True

            _tortoise_article = TortoiseArticleFactory(author__username="admin")
            _tortoise_user = TortoiseUserFactory(username="admin")

            # Testing SubFactory
            self.assertIsInstance(_tortoise_article.author, TortoiseUser)
            self.assertIsInstance(_tortoise_article, TortoiseArticle)
            self.assertIsInstance(_tortoise_user, TortoiseUser)
            self.assertIsInstance(
                _tortoise_article.author.id,  # type: ignore
                int,
            )
            self.assertIsInstance(
                _tortoise_article.author.is_staff,  # type: ignore
                bool,
            )
            self.assertIsInstance(
                _tortoise_article.author.date_joined,  # type: ignore
                datetime,
            )
            # Since we're mimicking Tortoise's behaviour, the following line
            # would fail on test, however would pass when testing against
            # real Tortoise model (as done in the examples).
            # self.assertEqual(_tortoise_article.author.username, "admin")

            # Testing Factory
            self.assertIsInstance(_tortoise_article.id, int)
            self.assertIsInstance(_tortoise_article.slug, str)
            self.assertIsInstance(_tortoise_user.id, int)
            self.assertIsInstance(_tortoise_user.username, str)

            # Testing hooks
            # self.assertFalse(
            #     hasattr(_tortoise_article, "_pre_save_called")
            # )
            # self.assertFalse(
            #     hasattr(_tortoise_article, "_post_save_called")
            # )

            # Testing batch creation
            _tortoise_articles = TortoiseArticleFactory.create_batch(5)
            self.assertEqual(len(_tortoise_articles), 5)
            self.assertIsInstance(_tortoise_articles[0], TortoiseArticle)

            # Testing traits
            _tortoise_admin_user = TortoiseUserFactory(is_admin_user=True)
            self.assertTrue(
                _tortoise_admin_user.is_staff
                and _tortoise_admin_user.is_superuser
                and _tortoise_admin_user.is_active
            )

        # **********************************
        # ***** SQLAlchemyModelFactory *****
        # **********************************

        class SQLAlchemySession:
            return_instance_on_query_first: bool = False

            def __init__(self) -> None:
                self.model = None
                self.instance = None

            def query(self, model) -> "SQLAlchemySession":
                self.model = model
                return self

            def filter_by(self, **kwargs) -> "SQLAlchemySession":
                return self

            def add(self, instance) -> None:
                self.instance = instance

            def commit(self) -> None:
                pass

            def first(self):
                if not self.return_instance_on_query_first:
                    return None

                return fill_dataclass(self.model)  # type: ignore

        def get_sqlalchemy_session():
            return SQLAlchemySession()

        @dataclass(frozen=True)
        class SQLAlchemyGroup:
            id: int
            name: str

        @dataclass
        class SQLAlchemyUser:
            """User model."""

            id: int
            username: str
            first_name: str
            last_name: str
            email: str
            date_joined: datetime = field(default_factory=datetime.utcnow)
            last_login: Optional[datetime] = None
            password: Optional[str] = None
            is_superuser: bool = False
            is_staff: bool = False
            is_active: bool = True
            groups: Set[SQLAlchemyGroup] = field(default_factory=set)

            def set_password(self, password: str) -> None:
                self.password = xor_transform(password)

        @dataclass
        class SQLAlchemyArticle:
            id: int
            title: str
            slug: str
            content: str
            headline: str
            category: str
            pages: int
            auto_minutes_to_read: int
            author: SQLAlchemyUser
            image: Optional[str] = (
                None  # Use str to represent the image path or URL
            )
            pub_date: date = field(default_factory=date.today)
            safe_for_work: bool = False
            minutes_to_read: int = 5

        def add_to_sqlalchemy_group(user: Any, name: str) -> None:
            group = SQLAlchemyGroupFactory(name=name)
            user.groups.add(group)

        class SQLAlchemyGroupFactory(SQLAlchemyModelFactory):
            id = FACTORY.pyint()  # type: ignore
            name = FACTORY.word()  # type: ignore

            class Meta:
                model = SQLAlchemyGroup
                get_or_create = ("name",)

            class MetaSQLAlchemy:
                get_session = get_sqlalchemy_session

        class SQLAlchemyUserFactory(SQLAlchemyModelFactory):
            id = FACTORY.pyint()  # type: ignore
            username = FACTORY.username()  # type: ignore
            first_name = FACTORY.first_name()  # type: ignore
            last_name = FACTORY.last_name()  # type: ignore
            email = FACTORY.email()  # type: ignore
            last_login = FACTORY.date_time()  # type: ignore
            is_superuser = False
            is_staff = False
            is_active = FACTORY.pybool()  # type: ignore
            date_joined = FACTORY.date_time()  # type: ignore
            password = PreSave(set_password, password="sest1234")
            group = PostSave(add_to_sqlalchemy_group, name="SestGroup1234")

            class Meta:
                model = SQLAlchemyUser
                get_or_create = ("username",)

            class MetaSQLAlchemy:
                get_session = get_sqlalchemy_session

            @trait
            def is_admin_user(self, instance: SQLAlchemyUser) -> None:
                instance.is_superuser = True
                instance.is_staff = True
                instance.is_active = True

            @pre_save
            def _pre_save_method(self, instance):
                instance._pre_save_called = True

            @post_save
            def _post_save_method(self, instance):
                instance._post_save_called = True

        class SQLAlchemyArticleFactory(SQLAlchemyModelFactory):
            id = FACTORY.pyint()  # type: ignore
            title = FACTORY.sentence()  # type: ignore
            slug = FACTORY.slug()  # type: ignore
            content = FACTORY.text()  # type: ignore
            headline = LazyAttribute(lambda o: o.content[:25])
            category = LazyFunction(partial(random.choice, categories))
            pages = FACTORY.pyint(min_value=1, max_value=100)  # type: ignore
            auto_minutes_to_read = PreInit(set_auto_minutes_to_read)
            image = FACTORY.png_file(storage=storage)  # type: ignore
            pub_date = FACTORY.date()  # type: ignore
            safe_for_work = FACTORY.pybool()  # type: ignore
            minutes_to_read = FACTORY.pyint(  # type: ignore
                min_value=1,
                max_value=10,
            )
            author = SubFactory(SQLAlchemyUserFactory)

            class Meta:
                model = SQLAlchemyArticle

            class MetaSQLAlchemy:
                get_session = get_sqlalchemy_session

            @pre_save
            def _pre_save_method(self, instance):
                instance._pre_save_called = True

            @post_save
            def _post_save_method(self, instance):
                instance._post_save_called = True

        with self.subTest("SQLAlchemyModelFactory"):
            _sqlalchemy_article = SQLAlchemyArticleFactory(
                author__username="admin"
            )

            # Testing SubFactory
            self.assertIsInstance(_sqlalchemy_article.author, SQLAlchemyUser)
            self.assertIsInstance(
                _sqlalchemy_article.author.id,  # type: ignore
                int,
            )
            self.assertIsInstance(
                _sqlalchemy_article.author.is_staff,  # type: ignore
                bool,
            )
            self.assertIsInstance(
                _sqlalchemy_article.author.date_joined,  # type: ignore
                datetime,
            )
            # Since we're mimicking SQLAlchemy's behaviour, the following line
            # would fail on test, however would pass when testing against real
            # SQLAlchemy model (as done in the examples).
            # self.assertEqual(sqlalchemy_article.author.username, "admin")

            # Testing Factory
            self.assertIsInstance(_sqlalchemy_article.id, int)
            self.assertIsInstance(_sqlalchemy_article.slug, str)

            # Testing PreInit
            self.assertEqual(
                _sqlalchemy_article.pages,
                _sqlalchemy_article.auto_minutes_to_read,
            )

            # Testing hooks
            self.assertTrue(
                hasattr(_sqlalchemy_article, "_pre_save_called")
                and _sqlalchemy_article._pre_save_called
            )
            self.assertTrue(
                hasattr(_sqlalchemy_article, "_post_save_called")
                and _sqlalchemy_article._post_save_called
            )

            # Testing batch creation
            _sqlalchemy_articles = SQLAlchemyArticleFactory.create_batch(5)
            self.assertEqual(len(_sqlalchemy_articles), 5)
            self.assertIsInstance(_sqlalchemy_articles[0], SQLAlchemyArticle)

            # Testing traits
            _sqlalchemy_admin_user = SQLAlchemyUserFactory(is_admin_user=True)
            self.assertTrue(
                _sqlalchemy_admin_user.is_staff
                and _sqlalchemy_admin_user.is_superuser
                and _sqlalchemy_admin_user.is_active
            )

            # Testing PreSave
            _sqlalchemy_user = SQLAlchemyUserFactory()
            self.assertEqual(
                xor_transform(str(_sqlalchemy_user.password)), "sest1234"
            )
            _sqlalchemy_user = SQLAlchemyUserFactory(
                password=PreSave(set_password, password="1234sest")
            )
            self.assertEqual(
                xor_transform(str(_sqlalchemy_user.password)), "1234sest"
            )

            # Testing PostSave
            self.assertEqual(
                list(_sqlalchemy_user.groups)[0].name,  # type: ignore
                "SestGroup1234",
            )
            _sqlalchemy_user = SQLAlchemyUserFactory(
                group=PostSave(add_to_sqlalchemy_group, name="1234SestGroup")
            )
            self.assertEqual(
                list(_sqlalchemy_user.groups)[0].name,  # type: ignore
                "1234SestGroup",
            )

            # Repeat SQLAlchemy tests for another condition
            SQLAlchemySession.return_instance_on_query_first = True

            _sqlalchemy_article = SQLAlchemyArticleFactory(
                author__username="admin"
            )
            _sqlalchemy_user = SQLAlchemyUserFactory(username="admin")

            # Testing SubFactory
            self.assertIsInstance(_sqlalchemy_article.author, SQLAlchemyUser)
            self.assertIsInstance(_sqlalchemy_article, SQLAlchemyArticle)
            self.assertIsInstance(_sqlalchemy_user, SQLAlchemyUser)
            self.assertIsInstance(
                _sqlalchemy_article.author.id,  # type: ignore
                int,
            )
            self.assertIsInstance(
                _sqlalchemy_article.author.is_staff,  # type: ignore
                bool,
            )
            self.assertIsInstance(
                _sqlalchemy_article.author.date_joined,  # type: ignore
                datetime,
            )
            # Since we're mimicking SQLAlchemy's behaviour, the following line
            # would fail on test, however would pass when testing against real
            # SQLAlchemy model (as done in the examples).
            # self.assertEqual(sqlalchemy_article.author.username, "admin")

            # Testing Factory
            self.assertIsInstance(_sqlalchemy_article.id, int)
            self.assertIsInstance(_sqlalchemy_article.slug, str)
            self.assertIsInstance(_sqlalchemy_user.id, int)
            self.assertIsInstance(_sqlalchemy_user.username, str)

            # Testing hooks
            self.assertFalse(hasattr(_sqlalchemy_article, "_pre_save_called"))
            self.assertFalse(hasattr(_sqlalchemy_article, "_post_save_called"))

            # Testing batch creation
            _sqlalchemy_articles = SQLAlchemyArticleFactory.create_batch(5)
            self.assertEqual(len(_sqlalchemy_articles), 5)
            self.assertIsInstance(_sqlalchemy_articles[0], SQLAlchemyArticle)

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


class TestSlugify(unittest.TestCase):
    def test_slugify_simple(self):
        """Test slugify with a simple alphanumeric string."""
        self.assertEqual(slugify("HelloWorld"), "helloworld")

    def test_slugify_spaces(self):
        """Test slugify with spaces."""
        self.assertEqual(slugify("Hello World"), "helloworld")

    def test_slugify_special_characters(self):
        """Test slugify with special characters."""
        self.assertEqual(
            slugify("Hello!@#$%^&*()_+World"),
            "helloworld",
        )

    def test_slugify_numbers(self):
        """Test slugify with numbers in the string."""
        self.assertEqual(slugify("H3llo W0rld123"), "h3llow0rld123")

    def test_slugify_empty_string(self):
        """Test slugify with an empty string."""
        self.assertEqual(slugify(""), "")

    def test_slugify_non_english_characters(self):
        """Test slugify with non-English characters."""
        self.assertEqual(slugify("Ողջույն, աշխարհ։"), "")

    def test_slugify_mixed_characters(self):
        """Test slugify with a mix of alphanumeric and special characters."""
        self.assertEqual(slugify("1234!@#$abcXYZ"), "1234abcxyz")
