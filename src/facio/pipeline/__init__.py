"""
.. module:: facio.pipeline
   :synopsis: Pipeline detection and execution.
"""

import yaml

from clint.textui import puts
from yaml.scanner import ScannerError


class Pipeline(object):

    def __init__(self, tpl_class):
        """ Pipeline class instanctiation.

        :param tpl_class: Template class instance,
        :type tpl_class: Object
        """

        self.tpl = tpl_class
        self._parse()

    def _parse(self):
        """ Parse the pipeline file. """

        with open(self.tpl.pipeline_file) as f:
            try:
                self.pipeline = yaml.load(f)
            except ScannerError:
                puts("Error loading Pipeline - Is it correctly formatted?")
            else:
                puts("Loading Pipeline")

    @property
    def has_before(self):
        """ Does the pipeline contain a before module list.

        :returns: Bool
        """

        return self.pipeline.get('before', False)
