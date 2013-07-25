# -*- coding: utf-8 -*-

"""
.. module:: facio.hooks.python.setup
   :synopsis: Bundled hooks for running python setup.py
"""

import os
import subprocess
import sys

from facio.base import BaseFacio
from facio.state import state


class Setup(BaseFacio):

    def log_errors(self, errors):
        """ Called with errors are encountered running setup.py and are logged
        to a setup.error.log.

        :param errors: Errors from setup.py
        :type errors: str
        """

        project_root = state.get_project_root()
        log_path = os.path.join(project_root, 'setup.error.log')

        with open(log_path, 'a') as handler:
            handler.write(errors)

        self.error('Errors detected with running setup.py, '
                   'please check {0}'.format(log_path))

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

    def get_default_path_to_python(self):
        """ Returns the default path to python, if virtualenv hooks
        has been called use that path, else use the current executing
        python, this should be the systems python in most cases.

        :returns: str -- path to python executable
        """

        # Returns path to virtualenv
        call = state.get_hook_call(
            'facio.hooks.python.virtualenv')

        if call:
            return os.path.join(call, 'bin', 'python')
        else:
            return sys.executable

    def get_path_to_python(self):
        """ Gets the path to python to run setup.py against.
        Detect if the virtualenv hooks has run, if so the default
        path to python should come from the path to this virtual environment,
        else it should be the system default python path.

        :returns: str -- The path to python
        """

        default = self.get_default_path_to_python()

        prompt = "Please enter the path to the python executable for running "\
                 "setup.py, leave blank to use: {0}: ".format(default)

        path = self.gather(prompt)
        if not path:
            path = default

        return path

    def run(self):
        """ Runs the python setup.py command.

        :returns: bool -- Based on return code subprocess call return code
        """

        project_root = state.get_project_root()
        working_dir = state.get_working_directory()

        python = self.get_path_to_python()
        setup = os.path.join(project_root, 'setup.py')
        arg = self.get_install_arg()

        self.out('Running: {0} ...'.format(' '.join([python, setup, arg])))

        os.chdir(project_root)
        call = subprocess.Popen([python, setup, arg],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        output, errors = call.communicate()
        os.chdir(working_dir)

        if call.returncode:
            self.log_errors(errors)
            return False

        return True


def run():
    """ Called by hooks runner, runs the setup class and returns Bool on
    status of the run command.

    :returns: bool -- The state of running setup.py
    """

    setup = Setup()
    return setup.run()
