from fake import FAKER, TextPdfGenerator

texts = FAKER.sentences()
pdf_file = FAKER.pdf_file(texts=texts, generator=TextPdfGenerator)

assert isinstance(pdf_file, str)
assert pdf_file.data["storage"].exists(pdf_file)
