Installing
==========

Facio can be installed on system using the standard python package installers
``pip`` or ``easy_install``.

.. note::

    ``sudo`` is used in the following commands for system wide installation.

Requirements
------------

Facio is written in python, the only requirement you need is to have one of the
following python versions installed.

* Python 2.6, 2.7, 3.2, 3.3

Pip or Easy Install
-------------------

.. code-block:: none

    sudo easy_install facio

or

.. code-block:: none

    sudo pip install facio

Manually
--------

.. code-block:: none

    cd /where/you/want/it/to/live
    git clone git@github.com:krak3n/facio.git
    cd facio
    sudo python setup.py install


Verify Install
--------------

Once you have installed ``Facio`` using one of the above methods you can very
the install by checking that the ``facio`` script was installed by running:

.. code-block:: none

    which facio
    > /usr/local/bin/facio

If all went well ``facio`` is now available from your command line.
