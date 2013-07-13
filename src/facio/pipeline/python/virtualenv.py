# -*- coding: utf-8 -*-

"""
.. module:: facio.pipeline.python.virtualenv
   :synopsis: Bundled pipeline for creating python virtual environments.
"""

from .. import BaseFacio


class Virtualenv(BaseFacio):

    def get_name(self):
        """ Returns the name for the virtualenv - gathered from user input with
        the default value being the project name from facio state.
        """

        pass

    def get_path(self):
        """ The path to where the virtual environment should be created, the
        user is prompted to input this path, default will be ~/.virtualenvs.
        """

        pass

    def create(self):
        """ Creates a python virtual environment. """

        pass


def run():
    """ Called from ``facio.pipeline`` runner.

    :returns: str -- Path to the created virtual environment
    """

    pass
