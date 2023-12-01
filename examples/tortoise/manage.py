#!/usr/bin/env python
import os
import sys

import IPython
from tortoise import Tortoise, run_async


async def init():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url="sqlite://tortoise_db.sqlite3",
        modules={"models": ["article.models"]},
    )
    # Generate the schema
    await Tortoise.generate_schemas()


def main():
    """Run administrative tasks."""
    sys.path.insert(0, os.path.abspath("."))
    run_async(init())
    IPython.embed()


if __name__ == "__main__":
    main()
