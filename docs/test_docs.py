import logging
from pathlib import Path
from unittest import mock
from unittest.mock import create_autospec

import pytest
from django.test import override_settings
from fake import FILE_REGISTRY

# Walk through the directory and all subdirectories for .py files
example_dir = Path("docs/_static/examples")
py_files = sorted([str(p) for p in example_dir.rglob("*.py")])


def execute_file(file_path, caplog):
    """Dynamic test function."""
    global_vars = {}
    # Set the log level to WARNING for this block
    with caplog.at_level(logging.WARNING):
        with open(file_path, "r") as f:
            code = f.read()
        exec(code, global_vars)


@pytest.mark.flaky(retries=3, delay=1)
@pytest.mark.django_db
@pytest.mark.parametrize("file_path", py_files)
def test_dynamic_files(file_path, caplog):
    execute_file(file_path, caplog)
    FILE_REGISTRY.clean_up()
