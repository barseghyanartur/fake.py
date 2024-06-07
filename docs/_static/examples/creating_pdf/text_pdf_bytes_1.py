from fake import FAKER, TextPdfGenerator

pdf_bytes = FAKER.pdf(generator=TextPdfGenerator)

assert isinstance(pdf_bytes, bytes)
