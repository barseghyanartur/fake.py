from fake import FAKER

texts = FAKER.sentences()
odt_bytes = FAKER.odt(texts=texts)
