# -*- coding: utf-8 -*-

"""
.. module:: facio.pipeline.python.virtualenv
   :synopsis: Bundled pipeline for creating python virtual environments.
"""

import os

from facio.base import BaseFacio
from facio.state import state


class Virtualenv(BaseFacio):

    def get_name(self):
        """ Returns the name for the virtualenv - gathered from user input with
        the default value being the project name from facio state.

        :returns: str -- Virtual environment name
        """

        project_name = state.get_context_variable('PROJECT_NAME')
        prompt = "Please enter a name for the virtual environment you want "\
                 "to create, leave blank to name it {0}: ".format(project_name)
        name = self.gather(prompt)
        if not name:
            name = project_name

        return name

    def get_path(self):
        """ The path to where the virtual environment should be created, the
        user is prompted to input this path, default will be ~/.virtualenvs.

        :returns: str -- The path to where the virtual environment
        """

        name = self.get_name()
        prompt = "Please enter the path of where to create the virtual "\
                 "environment or leave blank to create it in ~/.virtualenvs: "
        path = self.gather(prompt)
        if not path:
            path = os.path.join(os.path.expanduser('~'), '.virtualenvs')

        return os.path.join(path, name)

    def create(self):
        """ Creates a python virtual environment. """

        pass


def run():
    """ Called from ``facio.pipeline`` runner.

    :returns: str -- Path to the created virtual environment
    """

    pass
