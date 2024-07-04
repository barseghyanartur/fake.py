CLI
=============
All current providers are supported through CLI.

The entrypoint command is ``fake-py``.

----

Help
----
All commands overview
~~~~~~~~~~~~~~~~~~~~~
*Command*

.. code-block:: sh

    fake-py --help

*Output*

.. code-block:: sh

    usage: fake-py [-h]
                   {bmp,bmp_file,company_email,date,date_time,docx,docx_file,
                    domain_name,email,file_name,first_name,first_names,
                    free_email,free_email_domain,generic_file,gif,gif_file,
                    image,image_url,ipv4,last_name,last_names,name,names,
                    paragraph,paragraphs,pdf,pdf_file,png,png_file,pybool,
                    pydecimal,pyfloat,pyint,pystr,random_choice,random_sample,
                    sentence,sentences,slug,slugs,svg,svg_file,text,text_pdf,
                    text_pdf_file,texts,tld,txt_file,url,username,usernames,
                    uuid,uuids,word,words}
                   ...

    CLI for fake.py

    positional arguments:
      {bmp,bmp_file,company_email,date,date_time,docx,docx_file,domain_name,
       email,file_name,first_name,first_names,free_email,free_email_domain,
       generic_file,gif,gif_file,image,image_url,ipv4,last_name,last_names,
       name,names,paragraph,paragraphs,pdf,pdf_file,png,png_file,pybool,
       pydecimal,pyfloat,pyint,pystr,random_choice,random_sample,sentence,
       sentences,slug,slugs,svg,svg_file,text,text_pdf,text_pdf_file,texts,
       tld,txt_file,url,username,usernames,uuid,uuids,word,words}
                            Available commands
        bmp                 Create a BMP image of a specified size and color.
        bmp_file            Create a BMP image file of a specified size and
                            color.
        company_email       Generate a random company email.
        date                Generate random date between `start_date`
                            and `end_date`.
        date_time           Generate a random datetime between `start_date`
                            and `end_date`.
        docx                Create a DOCX document.
        docx_file           Create a DOCX document file.
        domain_name         Generate a random domain name.
        email               Generate a random email.
        file_name           Generate a random filename.
        first_name          Generate a first name.
        first_names         Generate a list of first names.
        free_email          Generate a random free email.
        free_email_domain   Generate a random free email domain.
        generic_file        Create a generic file.
        gif                 Create a GIF image of a specified size and color.
        gif_file            Create a GIF image file of a specified size and
                            color.
        image               Create an image of a specified format, size and
                            color.
        image_url           Generate a random image URL.
        ipv4                Generate a random IP v4.
        last_name           Generate a last name.
        last_names          Generate a list of last names.
        name                Generate a name.
        names               Generate a list of names.
        paragraph           Generate a paragraph.
        paragraphs          Generate a list of paragraphs.
        pdf                 Create a PDF document of a given size.
        pdf_file            Create a PDF file.
        png                 Create a PNG image of a specified size and color.
        png_file            Create a PNG image file of a specified size and
                            color.
        pybool              Generate a random boolean.
        pydecimal           Generate a random Decimal number.
        pyfloat             Generate a random float number.
        pyint               Generate a random integer.
        pystr               Generate a random string.
        random_choice
        random_sample
        sentence            Generate a sentence.
        sentences           Generate a list of sentences.
        slug                Generate a slug.
        slugs               Generate a list of slugs.
        svg                 Create an SVG image of a specified size and color.
        svg_file            Create an SVG image file of a specified size and
                            color.
        text                Generate a text.
        text_pdf            Create a PDF document of a given size.
        text_pdf_file       Create a text PDF file.
        texts               Generate a list of texts.
        tld                 Generate a random TLD.
        txt_file            Create a text document file.
        url                 Generate a random URL.
        username            Generate a username.
        usernames           Generate a list of usernames.
        uuid                Generate a UUID.
        uuids               Generate a list of UUIDs.
        word                Generate a word.
        words               Generate a list of words.

    options:
      -h, --help            show this help message and exit

----

Specific command help
~~~~~~~~~~~~~~~~~~~~~
Each command has help too.

*Command*

.. code-block::

    fake-py url --help

*Output*

.. code-block:: sh

    usage: fake-py url [-h] [--protocols PROTOCOLS] [--tlds TLDS] [--suffixes SUFFIXES]

    options:
      -h, --help            show this help message and exit
      --protocols PROTOCOLS
                            protocols (type: Optional[tuple[str, ...]])
      --tlds TLDS           tlds (type: Optional[tuple[str, ...]])
      --suffixes SUFFIXES   suffixes (type: Optional[tuple[str, ...]])

----

Common commands
---------------
company_email
~~~~~~~~~~~~~
**With defaults**

*Command*

.. code-block:: sh

    fake-py company_email

*Output*

.. code-block:: text

    michaelfrechet@right.com

**With customisations**

*Command*

.. code-block:: sh

    fake-py company_email --domain_names="github.com,microsoft.com"

*Output*

.. code-block:: text

    barrybaxter@github.com

----

date
~~~~
**With defaults**

*Command*

.. code-block:: sh

    fake-py date

*Output*

.. code-block:: text

    2024-06-21

----

**With customisations**

*Command*

.. code-block:: sh

    fake-py date --start_date="-7d" --end_date="7d"

*Output*

.. code-block:: text

    2024-07-04

----

docx_file
~~~~~~~~~
**With defaults**

*Command*

.. code-block:: sh

    fake-py docx_file

*Output*

.. code-block:: text

    tmp/tmp_0tnpurz.docx

----

**With customisations**

*Command*

.. code-block:: sh

    fake-py docx_file --nb_pages=100 --basename="my_docx_file"

*Output*

.. code-block:: text

    tmp/my_docx_file.docx

----

email
~~~~~
**With defaults**

*Command*

.. code-block:: sh

    fake-py email

*Output*

.. code-block:: text

    bad@not.org

**With customisations**

*Command*

.. code-block:: sh

    fake-py email --domain_names="github.com,microsoft.com"

*Output*

.. code-block:: text

    guess@github.com

----

url
~~~
**With defaults**

*Command*

.. code-block:: sh

    fake-py url

*Output*

.. code-block:: text

    http://one.com/lets.php

----

**With customisations**

*Command*

.. code-block:: sh

    fake-py url --tlds="am,nl,ie"

*Output*

.. code-block:: text

    https://readability.ie/face.go

----

slug
~~~~
*Command*

.. code-block:: sh

    fake-py slug

*Output*

.. code-block:: text

    unless-ambiguity-to-taaxihkoywxbolrienhq

----

text
~~~~
**With defaults**

*Command*

.. code-block:: sh

    fake-py text

*Output*

.. code-block:: text

    Should sparse and of idea. Is is is it than. Idea should is should
    explicitly. Are often practicality refuse than. Of the of in do.
    Is errors namespaces the better. Never to is do idea. The complicate.

----

**With customisations**

*Command*

.. code-block:: sh

    fake-py text --nb_chars=75

*Output*

.. code-block:: text

    Complicated is than explain right. Be silently better idea hard. Break than

----

username
~~~~~~~~
*Command*

.. code-block:: sh

    fake-py username

*Output*

.. code-block:: text

    better_if_great_ldffdumuptmqtzssjbgv

----

Customisation
-------------
By default, only standard (built-in) providers are available through CLI.

However, you can easily expose your providers via CLI too. See the
implementation below as an example.

*Filename: data.py*

.. literalinclude:: _static/examples/cli/data.py
    :language: python
    :lines: 173-175, 222-229, 275-281, 290-

*Filename: fake_address.py*

.. literalinclude:: _static/examples/cli/fake_address.py
    :language: python
    :lines: 1-6, 15-

*Filename: address_cli.py*

.. literalinclude:: _static/examples/cli/address_cli.py
    :language: python
    :lines: 1-

After that you can use it as follows:

.. code-block:: sh

    python address_cli.py --help
