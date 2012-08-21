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

    def should_exit_with_no_arguments(self):
        try:
            with nostdout():
                Config()
        except SystemExit:
            assert True

    def ensure_valid_project_name(self):
        with nostdout():
            sys.argv = ['', '-n', 'this_is_valid']
            c = Config()
        self.assertEquals(c.project_name, 'this_is_valid')
        with nostdout():
            sys.argv = ['', '-n', 'Thisisvalid']
            c = Config()
        self.assertEquals(c.project_name, 'Thisisvalid')

    def should_exit_on_invalid_name(self):
        try:
            with nostdout():
                sys.argv = ['', '-n', 'not-valid']
                Config()
        except SystemExit:
            assert True
        try:
            with nostdout():
                sys.argv = ['', '-n', 'not valid']
                Config()
        except SystemExit:
            assert True
        try:
            with nostdout():
                sys.argv = ['', '-n', 'not_valid-*']
                Config()
        except SystemExit:
            assert True
