#!/usr/bin/env python
import os
import sys

import IPython


def main():
    """Run administrative tasks."""
    sys.path.insert(0, os.path.abspath("."))
    IPython.embed()


if __name__ == "__main__":
    main()
