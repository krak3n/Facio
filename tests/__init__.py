"""
.. module:: tests
   :synopsis: Base test class.
"""

import os
import sys
import unittest

from mock import patch


class BaseTestCase(unittest.TestCase):

    IS_PY3 = sys.version_info[0] == 3

    test_tpl_path = os.path.join(
        os.path.abspath('.'),
        'tests',
        'files',
        'template')

    test_cfg_base_path = os.path.join(
        os.path.abspath('.'),
        'tests',
        'files',
        'configs')

    test_pieplines_path = os.path.join(
        os.path.abspath('.'),
        'tests',
        'files',
        'pipelines')

    def _test_cfg_path(self, fname):
        return os.path.join(self.test_cfg_base_path, fname)

    def _mock_std_out_in_err(self):
        self.patched_std_out = patch('sys.stdout')
        self.mocked_std_out = self.patched_std_out.start()
        self.patched_std_err = patch('sys.stderr')
        self.mocked_std_err = self.patched_std_err.start()
        self.patched_std_in = patch('sys.stdin')
        self.mocked_std_in = self.patched_std_in.start()

    def _mock_clint_start(self):
        """ Mock the clint.textui modules, clint_paths on self
        is required for this method to work. """

        self._mock_std_out_in_err()

        def effect(self, text):
            return text

        self.patched_ColoredString = patch(
            'clint.textui.colored.ColoredString', side_effect=effect)
        self.mocked_ColoredString = self.patched_ColoredString.start()

        try:
            for x, path in enumerate(self.clint_paths):
                name = path.replace('.', '_')
                if x == 0:
                    p = patch(path)
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
