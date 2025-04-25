from fake import FAKER, TextPdfGenerator

texts = ["Page 1 content", "Page 2 content", "Page 3 content"]
pdf_bytes = FAKER.pdf(texts=texts, generator=TextPdfGenerator)

assert isinstance(pdf_bytes, bytes)
