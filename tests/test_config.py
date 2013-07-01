# -*- coding: utf-8 -*-

"""
.. module:: tests.test_config
   :synopsis: Tests for the Facio config module.
"""

import os
import six

from mock import MagicMock, patch, PropertyMock
from facio.config import ConfigurationFile, CommandLineInterface, Settings
from facio.exceptions import FacioException
from six import StringIO
from textwrap import dedent

from . import BaseTestCase


class TestCommandLintInterface(BaseTestCase):

    def setUp(self):
        self._patch_clint([
            'facio.exceptions.puts',
        ])

    @patch('facio.config.docopt')
    @patch('facio.config.CommandLineInterface.validate_project_name')
    def test_project_name_should_be_validated(
            self,
            mock_validate,
            mock_docopt):
        mock_docopt.return_value = {
            '<project_name>': 'foo'
        }

        i = CommandLineInterface()
        i.start()

        mock_validate.assert_called_with('foo')

    def test_valid_project_name(self):
        valid_names = [
            'this_is_valid',
            'this1is_valid',
            'Thisisvalid']

        i = CommandLineInterface()

        for name in valid_names:
            self.assertTrue(i.validate_project_name(name))

    @patch('sys.exit')
    def test_invalid_project_name(self, mock_exit):
        invalid_names = [
            'this_is_not-valid',
            'this_is not_valid',
            '*this_is_not_valid']

        i = CommandLineInterface()

        for name in invalid_names:
            with self.assertRaises(FacioException):
                i.validate_project_name(name)
            self.mocked_facio_exceptions_puts.assert_any_call(
                'Error: Project names can only contain numbers letters and '
                'underscores')


class TestConfigurationFile(BaseTestCase):
    """ Tests for facio.config.ConfigurationFile. """

    config_path = os.path.expanduser('~/.facio.cfg')

    def setUp(self):
        self._patch_clint([
            'facio.config.puts',
            'facio.exceptions.puts',
        ])

    def _patch_exists(self):
        patcher = patch('facio.config.ConfigurationFile.exists',
                        return_value=True)
        self.addCleanup(patcher.stop)
        return patcher

    def _patch_open(self, data):
        if six.PY3:
            func = 'builtins.open'
        else:
            func = '__builtin__.open'
        patcher = patch(func, return_value=StringIO(
            data))
        self.addCleanup(patcher.stop)
        return patcher

    @patch('os.path.isfile', return_value=True)
    def test_exists_file_exists(self, mock_isfile):
        c = ConfigurationFile()
        self.assertTrue(c.exists('somefile.cfg'))

    @patch('os.path.isfile', return_value=False)
    def test_exists_file_does_not_exist(self, mock_isfile):
        c = ConfigurationFile()
        self.assertFalse(c.exists('somefile.cfg'))

    @patch('sys.exit')
    def test_config_read_parse_error(self, exit_mock):
        config = dedent("""\
        [this_is
        not = formatted
        correctly
        """)

        self._patch_exists().start()
        patch_open = self._patch_open(config)
        patch_open.start()

        with self.assertRaises(FacioException):
            c = ConfigurationFile()
            c.read()
        self.mocked_facio_exceptions_puts.assert_any_call(
            "Error: Unable to parse {0}".format(self.config_path))
        self.assertTrue(exit_mock.called)

    def test_config_read_success(self):
        config = dedent("""\
        [template]
        template1 = /foo/bar/baz
        template2 = /baz/bar/foo
        """)

        self._patch_exists().start()
        patch_open = self._patch_open(config)
        patch_open.start()

        c = ConfigurationFile()
        c.read()

        self.mocked_facio_config_puts.assert_any_call(
            "Loaded {0}".format(self.config_path))

    @patch('facio.config.ConfigurationFile.exists', return_value=False)
    def test_config_read_false_not_exists(self, mock_exists):
        c = ConfigurationFile()

        self.assertFalse(c.read())


class TestSettings(BaseTestCase):

    def setUp(self):
        self._patch_clint([
            'facio.config.puts',
            'facio.exceptions.puts',
        ])
        # Mocks for ConfigFile and CommandLineInterface classes
        self.mock_interface()
        self.config = MagicMock()

    def mock_interface(self):
        self.interface = MagicMock()
        arguments = PropertyMock(return_value={
            '<project_name>': 'foo'
        })
        type(self.interface).arguments = arguments

    def test_attrs_set_on_init(self):
        s = Settings(self.interface, self.config)

        self.assertIsInstance(s.config, MagicMock)
        self.assertIsInstance(s.interface, MagicMock)

    def test_retreive_project_name(self):
        s = Settings(self.interface, self.config)

        self.assertEqual(s.project_name, 'foo')

    @patch('sys.exit')
    def test_exception_no_project_name(self, mock_exit):
        s = Settings(self.interface, self.config)
        arguments = PropertyMock(return_value={})
        type(self.interface).arguments = arguments

        with self.assertRaises(FacioException):
            s.project_name
        self.mocked_facio_exceptions_puts.assert_any_call(
            "Error: Project name not defined.")
        self.assertTrue(mock_exit.called)


#import sys
#
#from docopt import DocoptExit
#from facio import config
#from facio.config import Config
#from mock import PropertyMock, patch
#
#from . import BaseTestCase
#
#
#class ConfigTests(BaseTestCase):
#    """ Argument Passing & Config Tests. """
#
#    base_args = ['test_skeleton', ]
#
#    def setUp(self):
#        """ Config Test Setup
#        Mocking stdout / stdin / stderr """
#
#        self.clint_paths = [
#            'facio.config.puts',
#        ]
#        self._mock_clint_start()
#        sys.argv = ['facio', ]
#        self._old_sys_argv = sys.argv
#
#    def tearDown(self):
#        sys.argv = self._old_sys_argv
#
#    def _set_cli_args(self, args):
#        sys.argv = ['facio', ] + args
#        self.config = Config()
#
#    def test_exit_with_no_arguments(self):
#        try:
#            Config()
#        except SystemExit:
#            assert True
#
#    @patch('facio.config.ConfigFile.path', new_callable=PropertyMock)
#    def test_cfg_is_not_loaded(self, mock_path):
#        mock_path.return_value = '/this/does/not/exist.cfg'
#        sys.argv = sys.argv + self.base_args
#        c = Config()
#
#        self.assertFalse(c.file_args.cfg_loaded)
#
#    @patch('facio.config.ConfigFile.path', new_callable=PropertyMock)
#    @patch('facio.config.blue')
#    def test_cfg_is_loaded(self, mock_blue, mock_path):
#        sys.argv = sys.argv + self.base_args
#        mock_path.return_value = self.empty_cfg
#        c = Config()
#        mock_blue.assert_called_with('Loaded ~/.facio.cfg')
#        self.assertTrue(c.file_args.cfg_loaded)
#
#    def test_valid_project_name(self):
#        valid_names = ['this_is_valid', 'this1is_valid', 'Thisisvalid']
#        for valid_name in valid_names:
#            try:
#                self._set_cli_args([valid_name, ])
#                self.assertEquals(self.config.project_name, valid_name)
#            except:
#                import ipdb
#                ipdb.set_trace()
#
#    def test_exit_on_invalid_name(self):
#        invalid_names = ['this_is_not-valid', 'this_is not_valid',
#                         '*this_is_not_valid']
#        for invalid_name in invalid_names:
#            try:
#                self._set_cli_args([invalid_name, ])
#            except (SystemExit, DocoptExit):
#                assert True
#            else:
#                assert False
#
#    def test_template_var_is_set_from_cli(self):
#        self._set_cli_args(self.base_args + ['--template',
#                                             self.test_tpl_path])
#        self.assertEquals(self.config.template, self.test_tpl_path)
#
#    @patch('facio.config.ConfigFile.path', new_callable=PropertyMock)
#    def test_exit_if_facio_cfg_is_miss_configured(self, mock_path):
#        cfgs = ['malformed_config1.cfg', 'malformed_config2.cfg']
#        for cfg in cfgs:
#            mock_path.return_value = self._test_cfg_path(cfg)
#            self._set_cli_args(self.base_args)
#            self.assertFalse(self.config.file_args.cfg_loaded)
#
#    @patch('facio.config.ConfigFile.path', new_callable=PropertyMock)
#    def test_valid_template_is_chosen_from_config(self, mock_path):
#        mock_path.return_value = self._test_cfg_path('multiple_templates.cfg')
#        config.input = lambda _: '2'
#        try:
#            self._set_cli_args(self.base_args + ['-s', ])
#            self.config = Config()
#            self.assertEquals(self.config.template, '/path/to/template')
#        except SystemExit:
#            pass  # We allow a pass here because the template path is invalid
#
#    def test_fail_if_invalid_template_choice(self):
#        config.input = lambda _: '8'
#        try:
#            self._set_cli_args(self.base_args + ['-s', ])
#            self.config = Config()
#        except SystemExit:
#            assert True
#
#    def test_value_error_raised_on_zero_template_choice(self):
#        config.input = lambda _: '0'
#        try:
#            self._set_cli_args(self.base_args + ['-s', ])
#            self.config = Config()
#        except SystemExit:
#            assert True
#
#    @patch('os.path.isdir', return_value=True)
#    @patch('facio.config.ConfigFile.path', new_callable=PropertyMock)
#    def test_can_refernce_template_by_name_from_cli(
#            self,
#            mock_path,
#            mock_isdir):
#        mock_path.return_value = self._test_cfg_path('multiple_templates.cfg')
#        try:
#            self._set_cli_args(self.base_args + ['-t', 'foo'])
#            self.config = Config()
#            self.assertEquals(self.config.template, '/path/to/template/foo')
#        except SystemExit:
#            assert False
#
#    @patch('facio.config.ConfigFile.path', new_callable=PropertyMock)
#    def test_can_refernce_template_by_name_from_cli_invalid(self, mock_path):
#        mock_path.return_value = self._test_cfg_path('multiple_templates.cfg')
#        try:
#            self._set_cli_args(self.base_args + ['-t', 'not_valid_name'])
#            Config()
#        except SystemExit:
#            assert True
#
#    def test_cache_django_secret_key(self):
#        sys.argv = sys.argv + self.base_args
#        self.config = Config()
#        key = self.config.django_secret_key
#        self.assertEquals(key, self.config.generated_django_secret_key)
#
#    def test_return_cached_version_of_secret_key(self):
#        sys.argv = sys.argv + self.base_args
#        self.config = Config()
#        self.config.generated_django_secret_key = 'this_is_cached'
#        self.assertEquals(self.config.django_secret_key, 'this_is_cached')
