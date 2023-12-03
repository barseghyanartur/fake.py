from fake import FAKER

texts = FAKER.sentences()
docx_bytes = FAKER.docx(texts=texts)
