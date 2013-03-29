Usage
=====

Facio is designed to be flexible to how you bootstrap your projects, heres how
to use it.

Basic Usage
-----------

Facio used via the command line, after installation you should have a ``facio`` command available. Use help to see the options available.

.. code-block:: none

    $ facio -h

To create a new project its simple, ``cd`` into the directory you want your new project to live, ``facio`` will create the directory for you so you don't need to make it, for example:

.. code-block:: none

    $ cd /home/me/projects
    $ facio -n hello_world

This will create a new ``hello_world`` directory at ``/home/me/projects`` and inside the default ``facio`` template will have been processed and placed there.
