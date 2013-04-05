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

Advanced Usage
--------------

Facio is designed to be flexible, with a combination of command line options
and a configuration file.

Command Line
^^^^^^^^^^^^

--version
            show program's version number and exit
-h, --help
            show this help message and exit

Project Options
***************

-n <ARG>, --name=<ARG>
            The Project Name (Mandatory), only use alphanumeric characters and underscores.

Template Options
****************

-t <ARG1>, --template=<ARG1>
            Path to your custom template, absolute paths only, git repositories can also be specified by prefixing with git+
            for example: git+git@gitbub.com/path/to/repo.git

-c, --choose_template
            If you have more than 1 template defined use this flag to override the default template, Note: specifying -t
            (--template) will mean this flag is ignored.

-s <ARG>, --template_settings_dir=<ARG>
            Template settings directory name

--vars=<ARG>
            Custom variables, e.g --vars hello=world,sky=blue

Experimental Options
********************

-i, --install
            Install the project onto your path, e.g python setup.py develop
-e, --venv_create
            Create python virtual environment
-p <ARG>, --venv_path=<ARG>
            Python virtualenv home directory
-S, --venv_use_site_packages
            Create python vittual environment without --no-site-packages
-x <ARG>, --venv_prefix=<ARG>
            Virtual environment name prefix

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

    [misc]
    install=0 # Experimental

    # Experimental
    [virutalenv]
    venv_create=1
    venv_path=/home/me/.virtualenvs/

Above is an example ``~/.facio.cfg`` file and contains a ``[misc]``, ``[virtualenv]``, and ``[template]`` sections. These sections and their allowed options allow you set defaults so when you run ``facio`` form the command line you need to keep specifying things like template path and virtual environment creation.

Available Options
*****************

* ``[template]``
    * **default**: Path to your custom template, prefix with ``git+`` to define git repository path.
    * **other_template**: Path to other template
* ``[misc]``
    * **install**: 0 or 1 - Run ``setup.py`` to install project onto python path using ``setup.py develop``
* ``[virtualenv]``
    * **venv_create**: 0 or 1 - Create python virtual environment
    * **venv_path**: Path to python virtual environments home, e.g ``/home/me/.virtualenvs/``
