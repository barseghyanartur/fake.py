from pathlib import Path

from fake import FAKER, FileSystemStorage, TextPdfGenerator

BASE_DIR = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd()  # noqa
MEDIA_ROOT = BASE_DIR / "media"

STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")

pdf_file = FAKER.pdf_file(generator=TextPdfGenerator, storage=STORAGE)

assert isinstance(pdf_file, str)
assert pdf_file.data["storage"].exists(pdf_file)
