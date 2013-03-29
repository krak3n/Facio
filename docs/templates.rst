Project Templates
=================

Project templates are simple the bare bones of your project with key parts
where you would put things like the project name replaced wit **Jinja2**
template syntax.

These templates can live locally on your file system or they can live on a
remote ``git`` repository. See :doc:`Usage </usage>` for more on this.

Basic Example
-------------

This is a basic ``HTML`` project template:

.. code-block:: html

    <html>
        <head>
            <title>{{ PROJECT_NAME }}</title>
        </head>
        <body>
            <h1>Hello world, I am {{ PROJECT_NAEME }}</h1>
        </body>
    </html>

In the above example ``{{ PROJECT_NAME }}`` will be replaced with what ever you
set the project name to be in the command, so for example: ``$ facio -n foo``
would result in ``{{ PROJECT_NAME }}`` being replaced by ``foo``.

Your project can be made up of any file types, any directory structure, it all
gets copied over and processed.

Custom Variables
----------------

Of course project name is not always enough and in these situations you can send extra variables to ``facio`` to use in the template processing. To do this run ``facio`` with the ``--vars`` flag passing a comma separated list, for example:

.. code-block:: none

     facio -n hello_world --vars foo=bar,something=else

Templates
^^^^^^^^^

Accessing these variables in templates is easy:

.. code-block:: none

    Hello World
    foo={{ foo }}
    something={{ something }}

As Jinja2 is used to render the templates, you can use conditions, and other Jinja2 functionality, for example:

.. code-block:: none

    {% if foo=='bar' %}
    Foo is bar
    {% else %}
    Foo is not bar
    {% endif %}

See the `Jinja2`_ Documentation.

Renaming Files / Directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can even rename a directory and/or file by using double underscores around the variable name, for example:

.. code-block:: none

    - /path/to/template/
      - __foo__/
        - another.txt
      - __foo__.txt
      - some_file.txt
      - some_other_file.txt

.. code-block:: none

    - /path/to/template/
      - bar/
        - another.txt
      - bar.txt
      - some_file.txt
      - some_other_file.txt


.. Links
.. _Jinja2: http://jinja.pocoo.org/docs/
