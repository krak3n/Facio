Installing
==========

Facio can be installed on system using the standard python package installers
``pip`` and ``easy_install``.

.. note::

    ``sudo`` is used in the following commands for system wide installation.

Easy Install
------------

``sudo easy_install facio``

Pip
---

``sudo pip install facio``

Manual
------

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
