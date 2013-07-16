# -*- coding: utf-8 -*-

"""
.. module:: facio.pipeline.python.setup
   :synopsis: Bundled pipeline for running python setup.py
"""

from facio.base import BaseFacio


class Setup(BaseFacio):

    def get_install_type(self):
        """ Gets the install type from the user, for example
        setup.py install or develop.

        :returns: str -- The install type
        """

        pass

    def get_path_to_python(self):
        """ Gets the path to python to run setup.py against.
        Detect if the virtualenv pipeline has run, if so the default
        path to python should come from the path to this virtual environment,
        else it should be the system default python path.

        :returns: str -- The path to python
        """

        pass

    def run(self):
        """ Runs the python setup.py command.
        """

        pass


def run():

    pass
