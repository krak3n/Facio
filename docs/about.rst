About
=====

Facio: /ˈfa.ki.oː/ - Latin, meaning to make, do, act, perform, cause, bring about.

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

Features
--------

* Support for multiple templates
* Store templates in ``git`` or ``mercurial`` repositories
* Add template logic using ``Jinja2``
* Ability to add before and after hooks called before or after the
  project is created.
* Add extra context-variables to your templates
* Bundled hooks include:

  * Create python virtual environments
  * Run python ``setup.py install | develop``
  * Generate Django Secret key for usage in Django settings modules

License
-------

See LICENSE file in the `Git Repository`_.

Authors
-------

See AUTHORS file in the `Git Repository`_.

Special Thanks
--------------

To the amazing Tech Team at `Poke London`_.
And thanks to Jack for helping me name it (and pointing out grammatical errors). <3.

.. Links

.. _Git Repository: https://github.com/krak3n/facio
.. _Poke London: http://pokelondon.com
