Hooks
=====

Facio has the ability for you to write hooks which are pieces of code that are
run either before or after the project template is rendered.

Hooks are defined on a per project basis and are set in a file which resides
in the project template itself. This file is called ``.facio.hooks.yml``. It is
a ``YAML`` formated file consisting of a ``before`` and an ``after`` list of
python dotted paths to code to run. For example:

.. code-block:: yaml

    before:
      - path.to.foo

    after:
      - path.to.bar

We will go into more detail about how to write your own later however for now
we will show you how to use the bundled hooks that come with Facio.

Bundled Hooks
-------------

Facio also has some bundled hooks you can use out of the box.

These will continue to grow and improve as Facio matures further. Currently
there are only ``python`` related hooks.

Django Secret Key
~~~~~~~~~~~~~~~~~

* **Path**: ``facio.hooks.django.secret``
* **Type**: before
* **Creates Context Variable**: ``{{ DJANGO_SECRET_KEY }}``

For ``Django`` projects a secret key is need to protect your project. Django
generates this for you when you run ``django-admin.py startproject`` for
example. Facio can also do this and add a new variable to the template context.

To use this create a ``.facio.hooks.yml`` file at the root of your project
template and add the following:

.. code-block:: yaml

    before:
      - facio.hooks.django.secret

And in your template you can use the ``{{ DJANGO_SECRET_KEY }}`` variable, for
example the secret key would normally go in ``settings.py``:

.. code-block:: python

    ...
    SECRET_KEY = 'DJANGO_SECRET_KEY'
    ..

.. _python-virtualenv-hook-label:

Python Virtual Environment Creation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Path**: ``facio.hooks.python.virtualenv``
* **Type**: before or after
* **Creates Context Variable**: none

Facio can automatically create a python virtual environment for your project.
Add this hook in either the ``before`` or ``after`` list.

.. code-block:: yaml

    after:
      - facio.hooks.python.virtualenv

Prompts
^^^^^^^

This hook will ask for the following information with sensible defaults set so
you can just press ``enter`` to skip.

* **Virtual environment name**

  * The name of the virtual environment to create
  * Default: Project Name defined when running ``$ facio``

* **Virtual environment path**

  * Where the virtual environment should be created on your file system
  * Default: ``~/.virtualenvs``

Python Package Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Path**: ``facio.hooks.python.setup``
* **Type**: after
* **Creates Context Variable**: none

This hook allows you to install your project as a python module provided your
project has a ``setup.py`` correctly configured in the templates root
directory.

.. note::

    Since your template is required to have been processed before this can be run
    you should only define this hook in the ``after`` list of
    ``~/.facio.hooks.yml``.

.. code-block:: yaml

    after:
      - facio.hooks.python.setup

Prompts
^^^^^^^

This hook will ask you for the following information with sensible defaults set
so you can just press ``enter`` to skip.

* **Python path**

  * Path on the file system to the python executable to run ``setup.py``
    against.
  * Default: The current python executable running ``facio`` or if the
    :ref:`python-virtualenv-hook-label` hook has been run it will be the path
    to the virtual environments python executable.

* **install or develop**

  * Install the package onto the python path or install it as an editable
    module
  * Default: ``develop``
