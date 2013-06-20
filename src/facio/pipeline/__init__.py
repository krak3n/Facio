"""
.. module:: facio.pipeline
   :synopsis: Pipeline detection and execution.
"""

import sys
import yaml

from clint.textui import puts
from importlib import import_module
from yaml.scanner import ScannerError


class Pipeline(object):

    def __init__(self, tpl_class):
        """ Pipeline class instanctiation.

        :param tpl_class: Template class instance,
        :type tpl_class: Object
        """

        self.calls = []
        self.tpl = tpl_class
        self._parse()

    def _parse(self):
        """ Parse the pipeline file. """

        with open(self.tpl.pipeline_file) as f:
            try:
                self.pipeline = yaml.load(f.read())
            except ScannerError:
                puts("Error loading Pipeline - Is it correctly formatted?")
            else:
                puts("Loading Pipeline")

    def _validate_before(self):
        if 'before' in self.pipeline:
            if not type(self.pipeline.get('before')) == list:
                puts('Ignoring before: should be a list')
                return False
            else:
                return True
        return False

    def _validate_after(self):
        if 'after' in self.pipeline:
            if not type(self.pipeline.get('after')) == list:
                puts('Ignoring after: should be a list')
                return False
            else:
                return True
        return False

    @property
    def has_before(self):
        """ Does the pipeline contain a before module list.

        :returns: Bool
        """

        try:
            return self._validate_before()
        except TypeError:
            return False

    @property
    def has_after(self):
        """ Does the pipeline contain a after module list.

        :returns: Bool
        """

        try:
            return self._validate_after()
        except TypeError:
            return False

    def import_module(self, path):
        """ Import module to run in before or post pipeline.

        :param path: The python path to the module
        :type path: str
        """

        try:
            module = import_module(path)
        except ImportError:
            puts('Failed to Load module: {0}'.format(path))
            return False
        else:
            puts('Loaded module: {0}'.format(path))
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
                puts('Error Running Module: Missing run() method.')
            except Exception:
                e = sys.exc_info()[1]
                traceback = sys.exc_info()[2]
                puts('Exeption caught in module: {0} line: {1}'.format(
                    e,
                    traceback.tb_lineno))
            self.calls.append({path: result})
            return result

    def has_run(self, path):
        """ Has a pipeline module run.

        :param path: The pipeline python module path
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

        for path in self.pipeline.get('before', []):
            self.run_module(path)

    def run_after(self):
        """ Run the after modules. """

        for path in self.pipeline.get('after', []):
            self.run_module(path)
