Developing / Contributing
=========================

Fancy helping out? Fork, commit, issue pull request :) Also please write some tests to prove your new bit of code works.

This project uses git flow, if you are not familiar please see `Git Flow`_. Under Git Flow master is the most stable branch, develop is where active development occurs so please contribute using the **develop** branch.

Vagrant
-------

I use `Vagrant`_ for my personal development so I have bundled it with the
repository. There are a few dependencies to how I have it setup.

* Vagrant 1.1+
* VirtualBox (what ever the latest is)
* Vagrant Guest Additions Plugin: ``vagrant plugin install vagrant-vbguest``
* Vagrant Salt Provisioner: ``vagrant plugin install vagrant-salt``

Once you have all the dependencies installed it should be a simple case of
running ``vagrant up`` at the root of the repository. Once it's finished you
should have a development environment with all of the ``facio`` dependencies
installed into python virtual environment. All you have to do is ``python
setup.py develop``.

.. _Git Flow: https://github.com/nvie/gitflow
.. _Vagrant: http://www.vagrantup.com/
