import sys
import unittest

from skeletor.config import Config

from .helpers import nostdout


class ConfigTests(unittest.TestCase):
    """ Argument Passing & Config Tests. """

    def setUp(self):
        self._old_sys_argv = sys.argv
        sys.argv = [self._old_sys_argv[0].replace('nosetests', 'skeletor')]

    def tearDown(self):
        sys.argv = self._old_sys_argv

    def _set_cli_args(self, args):
        with nostdout():
            sys.argv = sys.argv + args
            self.config = Config()

    def should_exit_with_no_arguments(self):
        try:
            with nostdout():
                Config()
        except SystemExit:
            assert True

    def ensure_valid_project_name(self):
        self._set_cli_args(['-n', 'this_is_valid'])
        self.assertEquals(self.config.project_name, 'this_is_valid')
        self._set_cli_args(['-n', 'Thisisvalid'])
        self.assertEquals(self.config.project_name, 'Thisisvalid')

    def should_exit_on_invalid_name(self):
        try:
            self._set_cli_args(['-n', 'this_is_not-valid'])
        except SystemExit:
            assert True
        try:
            self._set_cli_args(['-n', 'this_is not_valid'])
        except SystemExit:
            assert True
        try:
            self._set_cli_args(['-n', '*this_is_not_valid'])
        except SystemExit:
            assert True
