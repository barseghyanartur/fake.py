#!/usr/bin/env python
import argparse
import os
import sys
import unittest

import IPython


def run_tests():
    """Function to run tests in the article directory."""
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=".", pattern="tests.py")
    runner = unittest.TextTestRunner()
    runner.run(suite)


def main():
    """Run administrative tasks based on command line arguments."""
    sys.path.insert(0, os.path.abspath(os.path.join("..", "..")))
    sys.path.insert(0, os.path.abspath("."))
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
