from fake import FAKER

texts = FAKER.sentences()
odt_file = FAKER.odt_file(texts=texts)

assert isinstance(odt_file, str)
assert odt_file.data["storage"].exists(odt_file)
