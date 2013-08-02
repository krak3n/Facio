Configuration & Command Line
============================

Facio can be configured using a file called ``.facio.cfg`` and how Facio runs
can also be defined by the command line interface, we will take a look at the
command line first.

Command Line Options
--------------------

Facio is a simple command line application, and here is how you use it.

.. note::

    Through out this document ``$`` represents a terminal prompt.

Required Arguments
~~~~~~~~~~~~~~~~~~

The first argument you pass to the ``facio`` command must always be a project
name. For example:

.. code-block:: none

    $ facio hello_world

If no additional optional arguments are supplied then Facio will use it's
default template to create the project.

Optional Arguments
~~~~~~~~~~~~~~~~~~

Template
********

For Facio to use a different template than it's default you must pass either
following arguments:

* ``--template | -t`` or ``--select | -s``

``--template``
^^^^^^^^^^^^^^

The ``--template`` or it's short hand equivalent ``-t`` takes a string which
can be either of the following:

* A file system path the template, for example ``/home/me/template/template1``
* A ``git`` or ``mercurial`` repository, for examople:

  * ``git+git@hithub.com:me/template.git``
  * ``git+/path/to/local/template``
  * ``hg+user@someremote.com:me/template``
  * ``hg+/path/to/local/template``

* A template name defined in ``~/.facio.cfg``, see
  :ref:`configuration-file-label`.

For example:

.. code-block:: none

    $ facio foo -t /my/local/template
    $ facio bar -t git+git@github.com:krak3n/Facio-Django-Template.git
    $ facio baz -t django

``--select``
^^^^^^^^^^^^

The ``--select`` or it's ``-s`` short hand is used for selecting a template
thats defined in the ``'.facio.cfg`` configuration file, see
:ref:`configuration-file-label` section for more information on how to define
multiple templates.

For example:

.. code-block:: none

    $ facio foo --select

You will be given a prompt asking you to choose a template, once chosen
``facio`` will process the selected template.

Variables
*********

You may also need to define more variables to be used when rendering your
template. You can do this using the :ref:`vars-label` argument.

.. _vars-label:

``--vars``
^^^^^^^^^^

You can add extra variables to the context using  ``--vars`` optional argument.
This argument takes a string which should contain a comma delimited list of key
value pairs separated by an ``=`` operator.

For example:

.. code-block:: none

    $ facio foo -t bar --vars x=1,y=2,z=3

This above example would define 3 new context variables when rendering the
template with the fllowing values:

* x = 1
* y = 2
* z = 3

And could be used in templates as follows:

.. code-block:: html

    <html>
        </head>
            <title>{{ PROJECT_NAME }}</title>
        </head>
        <body>
            <h1>{{ PROJECT_NAME }}</h1>
            <ul>
                <li>X = {{ x ]}</li>
                <li>Y = {{ y ]}</li>
                <li>Z = {{ z ]}</li>
            </ul>
        </body>
    </html>

Other
*****

``--help``
^^^^^^^^^^

The ``--help`` or ``-h`` will trigger the ``facio`` help message describing
briefly all the options available to you.

``--version``
^^^^^^^^^^^^^

The ``--version`` argument will allow to see the current version of Facio you
are using.

.. _configuration-file-label:

Configuration File
------------------

You can also define a configuration file called ``.facio.cfg``. This
configuration file should live in your home directory with your other
``.`` (dot) files. This configuration file should be in an ``ini`` style
format.

For example:

.. code-block:: ini

    [section1]
    option = value

    [section2]
    option = value

``[template]`` Section
~~~~~~~~~~~~~~~~~~~~~~

The ``[template]`` section allows you to define in the ``.facio.cfg`` file
multiple templates you use on a regular basis so you can access them quickly
from ``facio``.

For example:

.. code-block:: ini

    [template]
    django = git+git@github.com:me/django-template.git
    rails = git+git@github.com:me/rails-template.git

``[files]`` Section
~~~~~~~~~~~~~~~~~~~

The ``[files]`` section allows you to customise what files from your get
template get copied and which files do not get rendered by ``jinja2``.

The ``files`` section takes 2 options:

* ``copy_ignore``: A comma separated list of glob patterns of files **not** to
  copy, for example you might not want to copy ``pyc`` files or ``.git`` etc
  files that maybe on the file system or in the repository. The default values
  for this are:

  * ``.git``
  * ``.hg``
  * ``.svn``
  * ``.DS_Store``
  * ``Thumbs.db``

* ``render_ignore``: A comma separated list of glob patterns of files **not**
  to render in the template engine, for example images such as ``jpeg``,
  ``gif`` and ``png`` files.

  * ``*.png``
  * ``*.gif``
  * ``*.jpeg``
  * ``*.jpg``

For example:

.. code-block:: ini

    [files]
    copy_ignore = .env,*.pyc
    render_ignore = .coverage,*.ico

In addition to the defaults ``facio`` would not copy over any file named
``.env`` or any file name ending in ``.pyc``. It would also not render in the
template engine in addition to the defau;lts any file names ``.coverage`` or
any file name ending in ``.ico``.
