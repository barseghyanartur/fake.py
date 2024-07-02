from fake import CLI
from override_default_data import FAKER


def main():
    cli = CLI(faker=FAKER)
    cli.execute_command()


if __name__ == "__main__":
    main()
