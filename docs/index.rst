Facio Documentation
===================

Facio: /ˈfa.ki.oː/ - Latin, meaning to make, do, act, perform, cause, bring about.

|PyPi_version| |PyPi_downloads|

Stable State
------------
|travis_master| |coveralls_master|

Development State
-----------------
|travis_develop| |coveralls_develop|

What is it?
-----------

If you work on quick turn around projects either at work or in your free time you might end up doing a lot of boiler plate cruft for your projects over and over, creating the same basic template. You might copy and paste this around, it might fall out of date, you might make improvements in a project but forget about them for the next.

``Facio`` gives you the ability to create a standard template (or templates) for your projects so you can bootstrap in one single command.

Originally developed with `Django`_ in mind you can use ``Facio`` for any type of project.

Supports
--------

* Python 2.6, 2.7, 3.2, 3.3

Features
--------

* Custom Templates
* Git support for remote templates
* Multiple templates
* `Jinja2`_ Templates
* Python virtualenv creation
* Configuration using ``.facio.cfg``

Topics
------

.. toctree::
    :maxdepth: 3

    installing
    usage
    templates
    developing
    changelog

License
-------

See LICENSE file in the `Git Repository`_.

Authors
-------

See LICENSE file in the `Git Repository`_.

Special Thanks
--------------

To the Tech Team at `Poke London`_ and the awesome `Jinja2`_.

And thanks to Jack for helping me name it (and pointing out grammatical errors). <3.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. Links

.. _Django: https://www.djangoproject.com/
.. _Travis CI: https://travis-ci.org/krak3n/Facio
.. _Jinja2: http://jinja.pocoo.org/docs/
.. _Git Repository: https://github.com/krak3n/facio
.. _Poke London: http://pokelondon.com

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

.. |coveralls_develop| image:: https://coveralls.io/repos/krak3n/Facio/badge.png?branch=develop
    :target: https://coveralls.io/r/krak3n/Facio?branch=develop
    :alt: Coder Coverage on Develop Branch

.. |travis_develop| image:: https://travis-ci.org/krak3n/Facio.png?branch=develop
    :target: https://travis-ci.org/krak3n/Facio
    :alt: Travis build status on Develop Branch
