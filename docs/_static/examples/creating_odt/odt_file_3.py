from fake import FAKER

odt_file = FAKER.odt_file(nb_pages=100)

assert isinstance(odt_file, str)
assert odt_file.data["storage"].exists(odt_file)
