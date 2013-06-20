Pipeline
========

``Facio`` supports the ability to add pre and post pipelines to be run before
and after the project generation is complete.

Adding ``pipelines`` is done on a project level inside the projects template in
a file called ``.facio.pipeline``. This should be a ``YAML`` formatted file, an
example is below:

.. code-block:: yaml

    before:
        - facio.pipeline.python.make_virtualenv
    after:
        - facio.pipeline.python.setup
        - your.path.python.module

The example above would create a python virtual environment before building the
project and then after run the ``python setup.py develop`` script and finally
runs a module not bundled with ``facio``.

Bundled Pipeline Modules
------------------------

``facio.pipeline.python.make_virtualenv``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will create a python virtual environment for you.

.. important::

    You must have ``vritualenv`` installed:
    https://pypi.python.org/pypi/virtualenv/1.9.1

When run you will be prompted for the following information:

* **Name**: The name of the virtualenv -- Default: the project name
* **Path**: Where to create the virtual environment -- Default: ~/.virtualenv
* **Use Site Packages [y/N]**: Run with ``--system-site-packages`` flag -- Default: N

``facio.pipeline.python.setup``
-------------------------------

Run the ``python setup.py (develop|install)`` command.

When run you will be prompted for the following information:

* **Python Executable**: Path to the python executable -- Default:
  ``/usr/bin/python``
* **Install as develop [Y/n]**: Install as development egg -- Default: Y

Create your own
---------------

It's easy to make your own custom pipeline modules to be used with ``facio``.
When a pipeline is loaded facio will attempt to execute a ``run`` method. So
all you need is a python module that is importable and a ``run`` method in that
module.

Example:
^^^^^^^^

.. code-block:: python

    def run():
        print __facio__.template.project_root

The above will print out the ``project_root``.
