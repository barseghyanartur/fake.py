from django.conf import settings
from fake import FAKER, FileSystemStorage, TextPdfGenerator

STORAGE = FileSystemStorage(root_path=settings.MEDIA_ROOT, rel_path="tmp")

pdf_file = FAKER.pdf_file(generator=TextPdfGenerator, storage=STORAGE)
