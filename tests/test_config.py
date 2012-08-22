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
        valid_names = ['this_is_valid', 'this_is_valid', 'Thisisvalid']
        for valid_name in valid_names:
            self._set_cli_args(['-n', valid_name])
            self.assertEquals(self.config.project_name, valid_name)

    def should_exit_on_invalid_name(self):
        invalid_names = ['this_is_not-valid', 'this_is not_valid',
                '*this_is_not_valid']
        for invalid_name in invalid_names:
            try:
                self._set_cli_args(['-n', invalid_name])
            except SystemExit:
                assert True
            else:
                assert False

    def ensure_template_var_is_set_from_cli(self):
        self._set_cli_args(self.base_args + ['--template', self.test_tpl_path])
        self.assertEquals(self.config.template, self.test_tpl_path)

    def should_raise_exit_if_template_section_is_not_list(self):
        try:
            self._set_cli_args(self.base_args)
            self.config.set_template_options('this is not a list')
        except SystemExit:
            assert True
        else:
            assert False

    def should_exit_if_skeletor_cfg_is_miss_configured(self):
        try:
            with nostdout():
                self._set_cli_args(self.base_args)
                self.config.set_attributes('not valid', {'not': 'valid'})
        except SystemExit:
            assert True
        else:
            assert False
