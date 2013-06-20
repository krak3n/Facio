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

    def _mock_clint_start(self):
        """ Mock the clint.textui modules, clint_paths on self
        is required for this method to work. """

        def effect(text):
            return text

        try:
            for path in self.clint_paths:
                name = path.replace('.', '_')
                setattr(self, 'patched_{}'.format(name),
                        patch(path, side_effect=effect))
                patcher = getattr(self, 'patched_{}'.format(name))
                setattr(self, 'mocked_{}'.format(name), patcher.start())
        except AttributeError:
            pass

    def _mock_clint_stop(self):
        """ Stop the patched clint.textui modules, clint_paths on self
        is required for this method to work. """

        try:
            for path in self.clint_paths:
                name = path.replace('.', '_')
                patcher = getattr(self, 'patched_{}'.format(name))
                patcher.stop()
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
