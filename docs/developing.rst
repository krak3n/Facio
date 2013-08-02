Contributing
============

Fancy helping out? Fork, commit, issue pull request :)

I can't guarantee I will accept your pull request but here some things to to
help:

* Ensure your code is to PEP8 standards
* Your pull requests adds a useful feature or fixes a bug
* Your code has unittests to ensure it works as it should
* Your code is documented so documentation can be auto generated us sphinx

I use `Git Flow`_ to develop this project, as such the branch structure is as
follows:

* Master: The current stable release, hotfixes come off this branch
* Develop: The current in development code, feature branches come off this
  branch
* feature/x: Feature branches should be named ``feature/my_feature_name``

So please create new features from the **develop** branch. Pull requests onto
master directly will **not be accepted** unless it is a hotfix.

Installing the Code
-------------------

.. note::

    This section assumes familiarity with python virtual environments and
    pythons virtual environment wrapper.

First create a fork of ``http://github.com/krak3n/facio`` so it's in your own
github account, then clone:

.. code-block:: none

    $ git clone git@github.com:you/facio.git

Once cloned switch to the develop branchL

.. code-block:: none

    $ git fetch --all
    $ git checkout develop

Create a python virtual environment:

.. code-block:: none

    $ virtualenv facio --no-site-packages
    $ workon facio

Now you can install the code as a development egg with the development
dependencies, this includes everything you need to run tests and debug code.

.. code-block:: none

    $ make develop

Facio and it's dependencies will not be installed into your virtual
environment.

Vagrant
-------

I use `Vagrant`_ for my personal development so I have bundled the facio
repository with a ``Vagrantfile``.

There are the following dependencies:

* Vagrant 1.1+
* VirtualBox (what ever the latest is)
* Vagrant Guest Additions Plugin: ``vagrant plugin install vagrant-vbguest``
* Vagrant Salt Provisioner: ``vagrant plugin install vagrant-salt``

Once you have all the dependencies installed it should be a simple case of
running ``vagrant up`` at the root of the repository. Once it's finished you
should have a development environment with all of the ``facio`` dependencies
installed into python virtual environment. All you have to do is run:

.. code-block:: none

    $ make develop

On the vagrant box.

.. _Git Flow: https://github.com/nvie/gitflow
.. _Vagrant: http://www.vagrantup.com/
