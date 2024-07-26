from fake import FAKER

odt_bytes = FAKER.odt()

assert isinstance(odt_bytes, bytes)
