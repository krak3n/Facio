# -*- coding: utf-8 -*-

"""
.. module:: facio.pipeline.python.setup
   :synopsis: Bundled pipeline for running python setup.py
"""

from facio.base import BaseFacio


class Setup(BaseFacio):

    def get_install_arg(self):
        """ Gets the install args from the user, for example
        setup.py install or develop.

        :returns: str -- The install type
        """

        prompt = "Please enter the setyup.py args (install or develop) "\
                 "[{0}/{1} tries]: "
        valid_args = ['install', 'develop']

        for x in range(1, 6):
            arg = self.gather(prompt.format(x, 5))
            if arg in valid_args:
                break
        else:
            self.error("You did not enter a valid setup.py arg")
            return None

        return arg

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
