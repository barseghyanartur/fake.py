from fake import FAKER

docx_file = FAKER.docx_file(nb_pages=100)

assert isinstance(docx_file, str)
assert docx_file.data["storage"].exists(docx_file)
