# -*- coding: utf-8 -*-

"""
.. module:: facio.state
   :synopsis: Facio state module, for accessing and maintaining state during
              the template generation process.
"""

import os

from facio.base import BaseFacio
from sh import pwd
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

        self.update_context_variables({'PROJECT_NAME': name})
        self.state.project_name = name

    def get_project_name(self):
        """ Return the project name stored in the state.

        :returns: str
        """

        return self.state.project_name

    def get_working_directory(self):
        """ Use the ``sh`` library to return the current working directory
        using the unix command ``pwd``.

        :returns: str
        """

        return '{0}'.format(pwd()).strip()

    def get_project_root(self):
        """ Return the project root, which is the current working directory
        plus the project name.

        :returns: str
        """

        return os.path.join(self.get_working_directory(),
                            self.get_project_name())

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

    def get_hook_call(self, module_path):
        """ Returns a hook call result, else returns false if the module
        path is not in the hook call list.

        :param module_path: The python dotted path to the module
        :type module_path: str

        :returns: Call result
        """

        try:
            calls = self.state.hook_calls
        except AttributeError:
            calls = []

        try:
            module, result = [(m, r) for m, r in calls if m == module_path][0]
        except IndexError:
            return None

        return result

    def save_hook_call(self, module_path, result):
        """ Saves a hook call to state

        :param module_path: The python dotted path to the module
        :type module_path: str

        :param result: The result of the module run() function
        :type result: Anything

        :returns: list -- The call list or tuples
        """

        try:
            calls = self.state.hook_calls
        except AttributeError:
            calls = []

        if not self.get_hook_call(module_path):
            calls.append((module_path, result))
            self.state.hook_calls = calls

        return calls


state = State()
