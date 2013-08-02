# -*- coding: utf-8 -*-

"""
.. module:: facio.hooks
   :synopsis: Hook detection and execution.
"""

import sys
import yaml

from facio.base import BaseFacio
from facio.state import state
from importlib import import_module
from yaml.scanner import ScannerError


class Hook(BaseFacio):

    def __init__(self):
        """ Hook class instanctiation. """

        self.calls = []

    def load(self, path):
        """ Parse the hooks file.

        :param path: Path to hooks file, locally
        :type path: str
        """

        try:
            with open(path) as f:
                try:
                    self.hooks = yaml.load(f.read())
                except ScannerError:
                    self.warning('Error loading {0} hooks - Is it '
                                 'correctly formatted?'.format(path))
                else:
                    self.out('Loading hooks')
        except IOError:
            self.warning('{0} not found'.format(path))

    def _validate_before(self):
        try:
            if 'before' in self.hooks:
                if not type(self.hooks.get('before')) == list:
                    self.warning('Ignoring before: should be a list')
                    return False
                else:
                    return True
            return False
        except AttributeError:
            return False

    def _validate_after(self):
        try:
            if 'after' in self.hooks:
                if not type(self.hooks.get('after')) == list:
                    self.warning('Ignoring after: should be a list')
                    return False
                else:
                    return True
            return False
        except AttributeError:
            return False

    def has_before(self):
        """ Does the hooks file contain a before list.

        :returns: Bool
        """

        try:
            return self._validate_before()
        except TypeError:
            return False

    def has_after(self):
        """ Does the hooks file contain a after list.

        :returns: Bool
        """

        try:
            return self._validate_after()
        except TypeError:
            return False

    def import_module(self, path):
        """ Import module to run in before or post hooks.

        :param path: The python path to the module
        :type path: str
        """

        try:
            module = import_module(path)
        except ImportError:
            self.error('Failed to Load module: {0}'.format(path))
            return False
        else:
            self.out('Loaded module: {0}'.format(path))
            return module

    def run_module(self, path):
        """ Run a before or after module.

        :param path: Path to the module
        :type module: str
        """

        module = self.import_module(path)
        result = None

        if module:
            try:
                result = module.run()
            except AttributeError:
                self.error('Error Running Module: Missing run() method.')
            except Exception:
                e = sys.exc_info()[1]
                traceback = sys.exc_info()[2]
                self.warning('Exeption caught in module: {0} line: {1}'.format(
                    e,
                    traceback.tb_lineno))
            self.calls.append({path: result})
            state.save_hook_call(path, result)
            return result

    def has_run(self, path):
        """ Has a hooks module run.

        :param path: The hooks python module path
        :type path: str

        :returns: False if not run else the modules returned data
        """

        try:
            data = [d for d in self.calls if path in d][0]
        except IndexError:
            return False
        else:
            return data[path]

    def run_before(self):
        """ Run the before modules. """

        for path in self.hooks.get('before', []):
            self.run_module(path)

    def run_after(self):
        """ Run the after modules. """

        for path in self.hooks.get('after', []):
            self.run_module(path)
