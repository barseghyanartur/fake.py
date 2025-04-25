from fake import FAKER

docx_bytes = FAKER.docx(nb_pages=100)

assert isinstance(docx_bytes, bytes)
