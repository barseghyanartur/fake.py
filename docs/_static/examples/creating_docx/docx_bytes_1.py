from fake import FAKER

docx_bytes = FAKER.docx()

assert isinstance(docx_bytes, bytes)
