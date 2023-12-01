from django.conf import settings
from fake import FAKER, TextPdfGenerator, FileSystemStorage

STORAGE = FileSystemStorage(root_path=settings.MEDIA_ROOT, rel_path="tmp")

pdf_file = FAKER.pdf_file(generator=TextPdfGenerator, storage=STORAGE)
