Test/coverage configuration tweaks
==================================

If you decide to include ``fake.py`` into your code/package, the
easiest way to get the ``fake.py`` tests running is to create a
sibling module named ``test_fake.py`` in the same directory where
the ``fake.py`` is, with the following content:

*Filename: test_fake.py*

.. code-block:: python
    :name: test_fakepy

    from fake import *  # noqa
