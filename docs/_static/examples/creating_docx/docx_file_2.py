from fake import FAKER

texts = FAKER.sentences()
docx_file = FAKER.docx_file(texts=texts)
