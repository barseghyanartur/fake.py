from fake import FAKER

png_bytes = FAKER.png()

assert isinstance(png_bytes, bytes)
