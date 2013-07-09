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

    def update_context_variables(self, dictionary):
        """ Update the context varaibles dict with new values.

        ** Usage: **

        .. code-block:: python

            from facio.state import state
            dictionary = {
                'bar': 'baz',
                'fib': 'fab',
            }
            state.update_context_variables(dictionary)

        :param dictionary: Dictionary of new key values
        :type dictionary: dict
        """

        try:
            dict1 = self.state.context_variables
        except AttributeError:
            self.state.context_variables = {}
            dict1 = self.state.context_variables
        dict2 = dictionary

        if isinstance(dict1, dict) and isinstance(dict2, dict):
            dict1.update(dict2)
            self.state.context_variables = dict1
        else:
            self.warning('Failed to update context variables with {0}'.format(
                dict2))

    def get_context_variables(self):
        """ Returns the current context variables at time of call.

        :retutns: dict
        """

        try:
            return self.state.context_variables
        except AttributeError:
            return {}

    def get_context_variable(self, name):
        """ Return a specific context variable value.

        :param name: Context variable name
        :type name: str

        :returns: str or None -- None if name not found in var list
        """

        variables = self.get_context_variables()
        return variables.get(name, None)

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
