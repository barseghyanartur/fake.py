from fake import FAKER, TextPdfGenerator

texts = FAKER.sentences()
pdf_bytes = FAKER.pdf(texts=texts, generator=TextPdfGenerator)
