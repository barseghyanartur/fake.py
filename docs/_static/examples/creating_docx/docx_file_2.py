from fake import FAKER

texts = FAKER.sentences()
docx_file = FAKER.docx_file(texts=texts)

assert isinstance(docx_file, str)
assert docx_file.data["storage"].exists(docx_file)
