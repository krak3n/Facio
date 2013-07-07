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
from six.moves import configparser as ConfigParser
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
            'facio.exceptions.puts',
            'facio.config.ConfigurationFile.out',
            'facio.config.ConfigurationFile.warning',
        ])

    def _patch_open(self, data):
        if six.PY3:
            func = 'builtins.open'
        else:
            func = '__builtin__.open'
        patcher = patch(func, return_value=StringIO(
            data))
        self.addCleanup(patcher.stop)
        return patcher

    def test_warning_no_config_file(self):
        c = ConfigurationFile()
        c.read()

        self.mocked_facio_config_ConfigurationFile_warning.assert_any_call(
            "{0} Not found".format(self.config_path))

    @patch('sys.exit')
    def test_config_read_parse_error(self, exit_mock):
        config = dedent("""\
        [this_is
        not = formatted
        correctly
        """)

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

        patch_open = self._patch_open(config)
        patch_open.start()

        c = ConfigurationFile()
        c.read()

        self.mocked_facio_config_ConfigurationFile_out.assert_any_call(
            "Loaded {0}".format(self.config_path))


class TestSettings(BaseTestCase):

    def setUp(self):
        self._patch_clint([
            'facio.exceptions.puts',
            'facio.config.Settings.out',
            'facio.config.Settings.warning',
            'facio.config.Settings.error',
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

        self.assertEqual(s.get_project_name(), 'foo')

    @patch('sys.exit')
    def test_exception_no_project_name(self, mock_exit):
        arguments = PropertyMock(return_value={})
        type(self.interface).arguments = arguments

        s = Settings(self.interface, self.config)

        with self.assertRaises(FacioException):
            s.get_project_name()
        self.mocked_facio_exceptions_puts.assert_any_call(
            "Error: Project name not defined.")
        self.assertTrue(mock_exit.called)

    @patch('sys.exit')
    def test_exception_raised_select_template_no_config(self, mock_exit):
        arguments = PropertyMock(return_value={
            '--select': True})
        type(self.interface).arguments = arguments
        self.config.items.side_effect = ConfigParser.NoSectionError('template')

        s = Settings(self.interface, self.config)

        with self.assertRaises(FacioException):
            with self.assertRaises(ConfigParser.NoSectionError):
                s.get_template_path()
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: Missing [template] section in Facio configuration file.')
        self.assertTrue(mock_exit.called)

    @patch('sys.exit')
    def test_default_template_returned_none_defined(self, mock_exit):
        arguments = PropertyMock(return_value={
            '--select': False})
        type(self.interface).arguments = arguments

        s = Settings(self.interface, self.config)
        path = s.get_template_path()

        self.assertEqual(Settings.default_template_path, path)

    def test_path_returned_if_not_alias(self):
        arguments = PropertyMock(return_value={
            '--template': '/foo/bar/baz'})
        type(self.interface).arguments = arguments

        s = Settings(self.interface, self.config)
        path = s.get_template_path()

        self.assertEqual(path, '/foo/bar/baz')

    def test_path_retuend_from_alias(self):
        arguments = PropertyMock(return_value={
            '--template': 'foobar'})
        type(self.interface).arguments = arguments
        self.config.items.return_value = [('foobar', '/foo/bar/baz')]

        s = Settings(self.interface, self.config)
        path = s.get_template_path()

        self.assertEqual(path, '/foo/bar/baz')

    @patch('facio.config.input')
    def test_template_selection_input_success(self, mock_input):
        arguments = PropertyMock(return_value={
            '--select': True})
        type(self.interface).arguments = arguments
        self.config.items.return_value = [
            ('foo', '/foo'),
            ('bar', '/bar'),
            ('baz', '/baz'),
        ]
        mock_input.return_value = 1

        s = Settings(self.interface, self.config)
        path = s.get_template_path()

        self.assertEqual(path, '/foo')

    @patch('sys.exit')
    @patch('facio.config.input')
    def test_template_selection_input_error(self, mock_input, mock_exit):
        arguments = PropertyMock(return_value={
            '--select': True})
        type(self.interface).arguments = arguments
        self.config.items.return_value = [
            ('foo', '/foo'),
        ]
        mock_input.return_value = 0

        s = Settings(self.interface, self.config)

        with self.assertRaises(FacioException):
            with self.assertRaises(ValueError):
                s.get_template_path()
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: A template was not selected')
        self.assertTrue(mock_exit.called)

    def test_get_variables_from_cli(self):
        arguments = PropertyMock(return_value={
            '--vars': 'foo=bar'})
        type(self.interface).arguments = arguments

        s = Settings(self.interface, self.config)

        self.assertEqual(s.get_variables(), {'foo': 'bar'})

    def test_empty_ignores_not_configured(self):
        self.config.get.side_effect = ConfigParser.NoSectionError('misc')

        s = Settings(self.interface, self.config)

        self.assertEqual(s.get_ignore_globs(), [])

    def test_ignores_returned_as_list(self):
        self.config.get.return_value = 'foo=bar,baz=foo'

        s = Settings(self.interface, self.config)

        self.assertEqual(s.get_ignore_globs(), ['foo=bar', 'baz=foo'])
