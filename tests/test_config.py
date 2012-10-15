import sys

from skeletor import config
from skeletor.config import Config

from .base import BaseTestCase
from .helpers import nostdout


class ConfigTests(BaseTestCase):
    """ Argument Passing & Config Tests. """

    base_args = ['-n', 'test_skeleton']

    def _set_cli_args(self, args):
        with nostdout():
            sys.argv = sys.argv + args
            self.config = Config(use_cfg=False)

    def should_exit_with_no_arguments(self):
        try:
            with nostdout():
                Config(use_cfg=False)
        except SystemExit:
            assert True

    def test_cfg_is_not_loaded(self):
        with nostdout():
            sys.argv = sys.argv + self.base_args
            self.config = Config(use_cfg=False)
            self.assertEquals(self.config.use_cfg, False)

    def test_cfg_is_loaded(self):
        with nostdout():
            sys.argv = sys.argv + self.base_args
            self.config = Config()
            self.assertEquals(self.config.use_cfg, True)

    def test_custom_cfg_path_is_set(self):
        with nostdout():
            sys.argv = sys.argv + self.base_args
            self.config = Config(config_path=self.empty_cfg)
            self.assertEquals(self.config.config_path, self.empty_cfg)

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

    def should_exit_when_venv_create_set_no_venv_path_set(self):
        try:
            with nostdout():
                self._set_cli_args(self.base_args + ['--venv_create', ])
        except SystemExit:
            assert True
        else:
            assert False

    def should_not_exit_when_venv_create_set_venv_path_set(self):
        try:
            with nostdout():
                self._set_cli_args(self.base_args + ['--venv_create',
                    '--venv_path', '/some/path'])
        except SystemExit:
            assert False
        else:
            assert True

    def ensure_valid_template_is_chosen_from_config(self):
        config.raw_input = lambda _: '2'
        try:
            with nostdout():
                self._set_cli_args(self.base_args + ['-c', ])
                self.config = Config(config_path=self.multiple_templates_cfg)
                self.assertEquals(self.config.template, '/path/to/template')
        except SystemExit:
            pass  # We allow a pass here because the template path is invalid

    def should_fail_if_invalid_template_choice(self):
        config.raw_input = lambda _: '8'
        try:
            with nostdout():
                self._set_cli_args(self.base_args + ['-c', ])
                self.config = Config(config_path=self.multiple_templates_cfg)
        except SystemExit:
            assert True

    def ensure_value_error_raised_on_zero_template_choice(self):
        config.raw_input = lambda _: '0'
        try:
            with nostdout():
                self._set_cli_args(self.base_args + ['-c', ])
                self.config = Config(config_path=self.multiple_templates_cfg)
        except SystemExit:
            assert True
