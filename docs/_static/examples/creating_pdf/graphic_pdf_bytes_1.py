from fake import FAKER, GraphicPdfGenerator

pdf_bytes = FAKER.pdf(generator=GraphicPdfGenerator)

assert isinstance(pdf_bytes, bytes)
