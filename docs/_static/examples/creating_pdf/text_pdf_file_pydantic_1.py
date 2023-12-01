from pathlib import Path

from fake import FAKER, FileSystemStorage, TextPdfGenerator

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR / "media"

STORAGE = FileSystemStorage(root_path=MEDIA_ROOT, rel_path="tmp")

pdf_file = FAKER.pdf_file(generator=TextPdfGenerator, storage=STORAGE)
