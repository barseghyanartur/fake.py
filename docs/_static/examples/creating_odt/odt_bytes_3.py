from fake import FAKER

odt_bytes = FAKER.odt(nb_pages=100)

assert isinstance(odt_bytes, bytes)