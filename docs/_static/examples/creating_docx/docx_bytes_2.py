from fake import FAKER

texts = FAKER.sentences()
docx_bytes = FAKER.docx(texts=texts)

assert isinstance(docx_bytes, bytes)
