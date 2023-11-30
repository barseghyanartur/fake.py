from fake import FAKER, TextPdfGenerator

texts = FAKER.sentences()
pdf_file = FAKER.pdf_file(texts=texts, generator=TextPdfGenerator)
