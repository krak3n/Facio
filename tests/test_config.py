import sys

from skeletor.config import Config

from .base import BaseTestCase
from .helpers import nostdout


class ConfigTests(BaseTestCase):
    """ Argument Passing & Config Tests. """

    base_args = ['-n', 'test_skeleton']

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

    def ensure_template_var_is_set_from_cli(self):
        self._set_cli_args(self.base_args + ['--template', self.test_tpl_path])
        self.assertEquals(self.config.template, self.test_tpl_path)
