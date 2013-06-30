"""
.. module:: tests
   :synopsis: Base test class.
"""

import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from mock import patch


class BaseTestCase(unittest.TestCase):

    test_tpl_path = os.path.join(
        os.path.abspath('.'),
        'tests',
        'files',
        'template')

    def _test_cfg_path(self, fname):
        return os.path.join(self.test_cfg_base_path, fname)

    def _patch_clint(self, paths=[]):
        """ Mock the clint.textui modules, clint_paths on self
        is required for this method to work. """

        def effect(self, text):
            return text

        self.patched_ColoredString = patch(
            'clint.textui.colored.ColoredString', side_effect=effect)
        self.mocked_ColoredString = self.patched_ColoredString.start()

        try:
            for x, path in enumerate(paths):
                name = path.replace('.', '_')
                p = patch(path)
                self.addCleanup(p.stop)
                setattr(self, 'patched_{0}'.format(name), p)
                patcher = getattr(self, 'patched_{0}'.format(name))
                setattr(self, 'mocked_{0}'.format(name), patcher.start())
        except AttributeError:
            pass

    @property
    def empty_cfg(self):
        return self._test_cfg_path('empty.cfg')

    @property
    def multiple_templates_cfg(self):
        return self._test_cfg_path('multiple_templates.cfg')

    @property
    def malformed_cfg(self):
        return self._test_cfg_path('malformed_config.cfg')
