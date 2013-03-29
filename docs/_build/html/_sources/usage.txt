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
