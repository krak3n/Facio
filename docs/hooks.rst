Hooks
=====

Facio has the ability for you to write hooks which are pieces of code that are
run either before or after the project template is rendered.

Hooks are defined on a per project basis and are set in a file which resides
in the project template itself. This file is called ``.facio.hooks.yml``. It is
a ``YAML`` formated file consisting of a ``before`` and an ``after`` list of
python dotted paths to code to run.

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
