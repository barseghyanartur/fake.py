Cheatsheet
==========
Scientific content
------------------
Tricks for scientific content generation.

DOI (Digital Object Identifier)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generate a fake DOI - a string formatted as `10.####/####-####`:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_doi
        :emphasize-lines: 1-

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
Generate a fake arXiv ID in the modern format (e.g., `2101.12345`):

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
        :emphasize-lines: 1-

        from fake import FAKER, StringTemplate

        article_title = FAKER.sentence(suffix="")
        # 'Preferably youre than is now'

        authors = [FAKER.name() for _ in range(3)]
        # ['Thomas Sajip', 'Ben Gust', 'Christian Dragon De Monsyne']

        journal = StringTemplate("Journal of {word} Studies")
        # 'Journal of Better Studies'

        publication_year = FAKER.year()
        # 2042

        keywords = FAKER.words()
        # ['Youre', 'Guess', 'Is', 'Lets', 'Of']

----

Generate fake a short abstract:

.. container:: jsphinx-toggle-emphasis

    .. code-block:: python
        :name: test_article_abstract
        :emphasize-lines: 3-

        from fake import StringTemplate

        abstract = StringTemplate(
            """
            {date(start_date="-7d")}

            # Title: {sentence(nb_words=6, suffix="")}

            ## Authors: {name}, {name}, {name}

            ## Abstract

            ### Introduction
            {text(nb_chars=1_000)}

            ### Objective
            {text(nb_chars=1_000)}

            ### Methods
            {text(nb_chars=1_000)}

            ### Results
            {text(nb_chars=1_000)}

            ### Conclusion
            {text(nb_chars=1_000)}

            Keywords: {word()}, {word()}, {word()}
            """
        )

Sample output:

.. code-block:: text

    2025-04-07

    # Title: Way although enough flat to is

    ## Authors: Nadeem Lumholt, Anthony Warsaw, Collin Polo

    ## Abstract

    ### Introduction
    Right easy to the better. Ugly flat the that better. Explain those break is the. Break than beats complex python. And better right to explicit. Explicit dense there idea to. Rules lets its special although. Those do although way silenced. Practicality unless although implementation preferably. Simple face complex explicit is. Peters way temptation better at. To although be explicit way. Unless more namespaces complex not. A it break than if. The break tim although idea. Idea often ambiguity do rules. Face honking those not complex. Rules hard is be obvious. Better unless is if rules. Is ugly implementation refuse more. Is complex python is implementation. Better than if purity should. Simple than the obvious the. Is may to explain rules. And complex better better of. Is by special better silently. There do arent readability explain. And although namespaces complex is. Should complex nested python than. Break never refuse guess way. One refuse tim unless unless. Do unless than than one.

    ### Objective
    Easy in arent the although. Explicit the explicit one may. Is readability it practicality better. Should than is better if. Unless should if never great. To to often than arent. Than better youre ambiguity may. Now are idea often tim. Nested obvious the errors refuse. A complicated is one preferably. Cases of namespaces youre never. That lets never counts silenced. The it better namespaces to. Only guess implementation is than. Errors at its purity idea. Than python never the may. More unless better to better. Better pass nested now unless. Flat way do the way. Is implementation easy although is. Explain do lets guess do. Is arent silenced than often. Be cases although way great. One explicit should never zen. Than special to not do. Never should errors than simple. Namespaces readability hard better readability. Be better the cases only. Special although implementation in simple. Explicit its than way a. First although more implicit ugly. It dutch ambiguity implementation namespaces..

    ### Methods
    Than preferably silently unless one. Obvious may is special than. Is better now than lets. It ugly to is guess. Counts than although implementation is. Better is dutch enough complex. Better beautiful purity arent to. Refuse may one if explain. Should than good to way. To better if although be. Is in may explain bad. There obvious that explicitly python. Its hard implicit cases obvious. Is explicit are its do. Good practicality although special purity. Is python rules is better. Peters practicality should peters purity. Special to by although complex. A the the of now. Better only is idea only. The rules although preferably youre. A the that if better. Now bad the than great. The preferably than nested that. Do unless if those special. Idea one is only the. In complex not to is. Obvious it first than better. Better to although is the. A better do easy explain. Arent only one those the. Be practicality the are is. The by it simple only. Flat bad than it temptation. Do is simple never o.

    ### Results
    If honking be implementation although. That unless hard dutch explicitly. Of never is if if. In good tim implicit is. Are is dense idea implementation. Pass to than easy implementation. Than special never first than. Refuse than ambiguity is face. Obvious sparse namespaces obvious the. Peters the bad do nested. Complicated refuse guess may by. It readability do cases there. Not be the is refuse. Readability easy explicitly and one. Practicality ambiguity is often implementation. Easy it more the not. One readability the the now. One better at if simple. Special there better easy better. Should silently great guess zen. Do explicit obvious ugly youre. One if silenced namespaces is. One zen more errors rules. Although explain may only to. Right are now easy should. To may in readability never. Purity do may more never. Great by better ugly should. Silently errors temptation guess than. Dutch one refuse now purity. Now the never better enough. In do of dense a. Counts one than to a. To a.

    ### Conclusion
    Lets than at never never. Is preferably good better explain. Never do youre dense ugly. Lets the rules now complicated. Preferably it better may way. The better at if those. Should flat than is beautiful. Beautiful way although youre ugly. Dutch better should readability peters. Is purity lets great of. Ugly preferably explicit way better. Namespaces idea than explain right. Is than silently unless tim. Be better never than better. Arent namespaces not may easy. Explicit never simple easy never. Is ambiguity unless now ambiguity. May nested is a silently. Than is than enough better. Unless than honking although good. Good guess better sparse complex. Sparse beats better a never. First first complex honking to. Zen should nested bad the. Implementation guess a explicitly be. Way those preferably complex than. Tim complex one only sparse. Is zen to than good. To if than to that. Better way dutch preferably it. Explicit than in than special. Now lets there than nested. Guess the readabil.

    Keywords: Good, Unless, The
