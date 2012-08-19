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
