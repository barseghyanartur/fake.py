from fake import FAKER, TextPdfGenerator

pdf_bytes = FAKER.pdf(nb_pages=100, generator=TextPdfGenerator)
