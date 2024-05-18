"""
Configuration hooks for `pytest`. Normally this wouldn't be necessary,
but since `pytest-rst` is used, we want to clean-up files generated by
running documentation tests. Therefore, this hook, which simply
calls the `clean_up` method of the `FILE_REGISTRY` instance.
"""

import pytest
from fake import FILE_REGISTRY

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2024 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "pytest_runtest_setup",
    "pytest_runtest_teardown",
)


def pytest_collection_modifyitems(session, config, items):
    """Modify test items during collection."""
    for item in items:
        try:
            from pytest_rst import RSTTestItem

            if isinstance(item, RSTTestItem):
                # Dynamically add marker to RSTTestItem tests
                item.add_marker(pytest.mark.django_db(transaction=True))
        except ImportError:
            pass


def pytest_runtest_setup(item):
    """Setup before test runs."""
    try:
        from pytest_rst import RSTTestItem

        if isinstance(item, RSTTestItem):
            pass
    except ImportError:
        pass


def pytest_runtest_teardown(item, nextitem):
    """Clean up after test ends."""
    try:
        from pytest_rst import RSTTestItem

        if isinstance(item, RSTTestItem):
            FILE_REGISTRY.clean_up()
    except ImportError:
        pass