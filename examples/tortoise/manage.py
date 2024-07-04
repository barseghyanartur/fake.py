#!/usr/bin/env python
import argparse
import os
import sys
import unittest

import IPython
from tortoise import Tortoise, run_async


def run_tests():
    """Function to run tests in the article directory."""
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="./article", pattern="tests.py")
    runner = unittest.TextTestRunner()
    runner.run(suite)


async def init():
    # Initialise SQLite DB and specify the app name of "models"
    #  alongside the models "article.models"
    await Tortoise.init(
        db_url="sqlite://:memory:",
        # db_url="sqlite://tortoise_db.sqlite3",
        modules={"models": ["article.models"]},
    )
    # Generate the schema
    await Tortoise.generate_schemas()


def main():
    """Run administrative tasks."""
    sys.path.insert(0, os.path.abspath(os.path.join("..", "..")))
    sys.path.insert(0, os.path.abspath("."))
    run_async(init())

    parser = argparse.ArgumentParser(
        description="Management script for the project."
    )
    parser.add_argument("command", help="The command to run (test or shell)")

    args = parser.parse_args()

    if args.command == "test":
        run_tests()
    elif args.command == "shell":
        IPython.embed()
    else:
        print("Unknown command. Use 'test' or 'shell'.")


if __name__ == "__main__":
    main()
