Cheat sheet
===========
Scientific content
------------------
Quick tricks for generating scientific content.

DOI (Digital Object Identifier)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generate a fake DOI - a string formatted as ``10.####/####-####``:

.. code-block:: python
    :name: test_doi

    from fake import FAKER

    FAKER.randomise_string(value="10.####/####-####")
    # '10.4613/4636-8596'

----

ISSN/EISSN (International/Electronic Serial Number)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generate a fake ISSN/EISSN - a string of eight digits with a hyphen between
the groups of four digits:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_issn_eissn
        :emphasize-lines: 3-

        from fake import FAKER

        FAKER.randomise_string(value="####-####")
        # '6160-6320'

----

ORCID (Open Researcher and Contributor ID)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generate a fake ORCID ID - four groups of four digits separated by hyphens:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_orchid_id
        :emphasize-lines: 3-

        from fake import FAKER

        FAKER.randomise_string(value="####-####-####-####")
        # '6827-5849-5672-2984'

----

arXiv Identifier
~~~~~~~~~~~~~~~~
Generate a fake arXiv ID in the modern format (e.g., ``2101.12345``):

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_arxiv_id
        :emphasize-lines: 3-

        from fake import FAKER

        FAKER.randomise_string(value="####.#####")
        # '0206.74568'

----

Scientific article metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generate fake metadata for a scientific article, including a title, a
list of authors, journal name, publication year, and keywords:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_article_metadata
        :emphasize-lines: 3-

        from fake import FAKER

        article_title = FAKER.sentence(suffix="")
        # 'Preferably youre than is now'

        authors = [FAKER.name() for _ in range(3)]
        # ['Thomas Sajip', 'Ben Gust', 'Christian Dragon De Monsyne']

        journal = FAKER.string_template("Journal of {word} Studies")
        # 'Journal of Better Studies'

        publication_year = FAKER.year(start_year=1970, end_year=2024)
        # 2001

        keywords = FAKER.words()
        # ['Youre', 'Guess', 'Is', 'Lets', 'Of']

----

Generate a fake short abstract:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_article_abstract
        :emphasize-lines: 3-

        from fake import FAKER

        abstract = FAKER.string_template(
            """
            {date(start_date="-7d")}

            # Title: {sentence(nb_words=6, suffix="")}

            ## Authors: {name}, {name}, {name}

            ## Abstract

            ### Introduction
            {text(nb_chars=200, allow_overflow=True)}

            ### Objective
            {text(nb_chars=200, allow_overflow=True)}

            ### Methods
            {text(nb_chars=200, allow_overflow=True)}

            ### Results
            {text(nb_chars=200, allow_overflow=True)}

            ### Conclusion
            {text(nb_chars=200, allow_overflow=True)}

            Keywords: {word}, {word}, {word}
            """
        )

Sample output:

.. code-block:: text

    2025-04-08

    # Title: Of dutch a cases silenced never

    ## Authors: Michael Dalke, Barry Dragon De Monsyne, Victor Diederich

    ## Abstract

    ### Introduction
    Implicit idea of better idea. And special errors implicit is. Is are
    explicit better complicated. More nested cases honking lets. Never of
    beautiful than be. Explicit way namespaces better explicitly.

    ### Objective
    Better implementation it complex by. Way bad preferably do a. Is than
    temptation good although. The guess if ambiguity the. Better its sparse
    and special. Is than is preferably than. Of although do to practicality.

    ### Methods
    Should its than flat to. There than explicit obvious at. Idea readability
    idea is ugly. Only refuse now the now. Complex its one complicated of. The
    flat obvious temptation dutch. Flat is python tim simple.

    ### Results
    Way there guess than to. Pass is and are beautiful. It nested that
    although obvious. Better better simple idea than. Is not better great
    simple. The complex although explain of. Than special than than obvious.

    ### Conclusion
    Explicitly explain more enough honking. To counts dense should pass.
    Obvious unless is if be. Be implementation good implementation now.
    Better if than now face. At complex to although than. Than may of better.

    Keywords: Do, Lets, Unlessd, Purity, Complex
