from fake import FAKER, TextPdfGenerator

pdf_file = FAKER.pdf_file(nb_pages=100, generator=TextPdfGenerator)

assert isinstance(pdf_file, str)
assert pdf_file.data["storage"].exists(pdf_file)
