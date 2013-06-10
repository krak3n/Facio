Usage
=====

Facio is designed to be flexible to how you bootstrap your projects, heres how
to use it.

Out of the box
--------------

Facio used via the command line, after installation you should have a ``facio`` command available. Use help to see the options available.

.. code-block:: none

    $ facio -h

To create a new project its simple, ``cd`` into the directory you want your new project to live, ``facio`` will create the directory for you so you don't need to make it, for example:

.. code-block:: none

    $ cd /home/me/projects
    $ facio -n hello_world

This will create a new ``hello_world`` directory at ``/home/me/projects`` and inside the default ``facio`` template will have been processed and placed there.

Supported VCS
^^^^^^^^^^^^^

In addition to local file paths you can also use a ``VCS`` repository to use as
your templates location. Currently ``facio`` supports:

* **Git**: Add ``git+`` followed by the remote path to the repository, for
  example: ``git+git@gitbub.com/path/to/repo.git``.
* **Mercurial**: Add ``hg+`` followed by the remote path to the repository, for
  example: ``hg+you@bitbucket.com/path/to/repo``.

Command Line Usage
^^^^^^^^^^^^^^^^^^

.. program:: facio

.. cmdoption:: -h, --help

   Show the help message

.. cmdoption:: --version

    Show version

.. cmdoption:: -t <path>, --template <path>

    Template path, can be repository link (git+ / hg+) or a template name defined in ~/.facio.cfg.

.. cmdoption:: -s, --select

    Lists templates in ~/.facio.cfg prompting you to select a template from this list.

.. cmdoption:: --vars <variables>

    Comma separated key=value pairs of values to be used in processing templates.

Example
*******

.. code-block:: none

    facio hello_world -t git+git@github.com:you/django.git --vars foo=bar


Configuration File
^^^^^^^^^^^^^^^^^^

Most things you can specify as command line options are also configurable in a ``facio.cfg`` file, this should live in your home directory and be prefixed with a ``.``, for example ``/home/you/.facio.cfg``.

Example ``~/.facio.cfg``
************************

The ``~/.facio.cfg`` file uses ``ini`` style formatting.

.. code-block:: none

    [template]
    # The Default Template to user (can be a git repp, prefix with git+url_to_repo
    default=/home/me/my_custom_template/
    # Add other templates here, for example:
    experimental_template: /my/new/template/
    flask: git+git@github.com/my_flask_template.git
    mercurial: hg+you@bitbucket.com/my_mercurial_template.git

    [misc]
    ignore='*.gif','./[0-9].*','?.png'

Above is an example ``~/.facio.cfg`` file and contains a ``[misc]`` and ``[template]`` sections. These sections and their allowed options allow you set defaults so when you run ``facio`` form the command line you need to keep specifying things like templates.

Available Options
*****************

* ``[template]``
    * **default**: Path to your custom template, prefix with ``git+`` to define git repository path.
    * **other_template**: Path to other template
* ``[misc]``
    * **ignore**: A comma separated list of globs which specify a pattern of
      files to ignore, for example ``'*.gif'`` would ignore all files with a gif
      extenstion.
