Quick Start
===========

Facio is designed to simple and easy and also flexible. Here is how to use it:

Out of the box
--------------

Facio is a command line application, after you have installed Facio you should
now have a ``facio`` command available on your command line. You can use it
straight away without any configuration. It won't give you anything useful but
you can see the basics of how Facio works.

Lets create a new project called foo:

.. note::

    ``$`` denotes your shell prompt throughout this page

.. code-block:: none

    $ facio foo

The above command will bootstrap a very simple sample project which is
bundled with Facio and just contains some HTML and CSS. It will be
created in the directory in which the ``facio`` command was run and be called
``foo``.

You should be able to open this in a web browser to see more information about
Facio.

But this isn't particularly useful for building your skeleton so let's go on.

Your First Template (Skeleton)
------------------------------

We will call project skeletons templates. These templates are designed for
reuse and should be kept maintained and updated as you learn new and better
ways of creating your projects.

Let's keep it simple to start with by creating a simple HTML project template.

Create a new directory somewhere on your system and lets call it ``html_template``.
Inside it make 1 html file, you can call it whatever you like but for sanity we
will refer to it as ``index.html``. Now inside this file add the following:

.. code-block:: html

    <html>
        <head>
            <title>{{ PROJECT_NAME }}</title>
        </head>
        <body>
            <h1>Welcome to {{ PROJECT_NAME|upper() }}</h1>
            <p>My first Facio generated project template!</p>
        </body>
    </html>

Now let's tell Facio to use this template: change to a new directory where you
would like the project to be created and run:

.. code-block:: none

    $ facio bar -t /path/to/html_template

A new directory will be created called ``bar`` in your current working
directory and inside you'll find ``index.html`` with the following content:

.. code-block:: html

    <html>
        <head>
            <title>bar</title>
        </head>
        <body>
            <h1>Welcome to BAR</h1>
            <p>My first Facio generated project template!</p>
        </body>
    </html>

You'll notice that because we used one of Jinja2's builtin filters, ``upper``
in the ``h1`` tags, the project name has been capitalised.

A full list of built in Jinja2 filters can be found `here
<http://jinja.pocoo.org/docs/templates/#builtin-filters>`_.
