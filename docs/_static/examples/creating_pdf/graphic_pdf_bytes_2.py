from fake import FAKER, GraphicPdfGenerator

pdf_bytes = FAKER.pdf(nb_pages=100, generator=GraphicPdfGenerator)
