Facio
=====

Facio: /ˈfa.ki.oː/ - Latin, meaning to make, do, act, perform, cause, bring about.

|PyPi_version| |PyPi_downloads| |travis_master| |coveralls_master|

What is it?
-----------

Are you forever creating new projects, re creating the same standard cruft over
and over? Then Facio maybe for you, it allows you to create your standard
project skeleton once and create new projects from that standard skeleton over
and over, easily.

It can be as simple or as complicated as you need it to be. You can write logic
into your skeleton, store it in a ``git`` or ``mercurial`` repository, you can
even write hooks to be run before or after your skeletons been built. Did I
mention you can have as many templates as you like and quickly reference them
by name or pick from a list.

Facio aims to hopefully fix your standard project skeleton woes.

.. code-block:: none

    facio my_new_project -t django_skeleton

Supports
--------

* Python 2.6, 2.7, 3.2, 3.3

Features
--------

* Support for multiple templates
* Store templates in ``git`` or ``mercurial`` repositories
* Add template logic using ``Jinja2``
* Add extra context-variables to your templates
* Ability to add before and after hooks that are called before or after the
  project is created.
* Bundled hooks include:

  * Create python virtual environments
  * Run python ``setup.py install | develop``
  * Generate Django Secret key for usage in Django settings modules

Documentation
-------------

Documentation for ``Facio`` can be found on here on `Read the Docs`_.

.. Links

.. _Read the Docs: https://facio.readthedocs.org

.. Images

.. |PyPi_version| image:: https://pypip.in/v/facio/badge.png
    :target: https://crate.io/packages/facio/
    :alt: Latest PyPI version

.. |PyPi_downloads| image:: https://pypip.in/d/facio/badge.png
    :target: https://crate.io/packages/facio/
    :alt: Number of PyPI downloads

.. |coveralls_master| image:: https://coveralls.io/repos/krak3n/Facio/badge.png?branch=master
    :target: https://coveralls.io/r/krak3n/Facio?branch=master
    :alt: Latest PyPI version

.. |travis_master| image:: https://travis-ci.org/krak3n/Facio.png?branch=master
    :target: https://travis-ci.org/krak3n/Facio
    :alt: Travis build status on Master Branch
