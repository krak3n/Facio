# -*- coding: utf-8 -*-

"""
.. module:: facio.state
   :synopsis: Facio state module, for accessing and maintaining state during
              the template generation process.
"""

from facio.base import BaseFacio
from six.moves import builtins


class State(BaseFacio):

    def __init__(self):
        """ State is stored in a __facio__ super global set at the moment
        this class is instantiated but only if not already set.

        This class is basically a proxy class for interfacing with __facio__
        super global variable. All state is set and retrieved from __facio__.
        """

        try:
            self.state = builtins.__facio__
        except AttributeError:
            builtins.__facio__ = self
            self.state = builtins.__facio__

    def set_project_name(self, name):
        """ Set the project name to the state.

        :param name: The project name from facio.config.CommandLineInterface
        :type name: str
        """

        self.state.project_name = name

    def get_project_name(self):
        """ Return the project name stored in the state.

        :returns: str
        """

        return self.state.project_name


state = State()
