# -*- coding: utf-8 -*-

"""
.. module:: tests.test_pipeline.test_python
   :synopsis: Tests for bundled python pipelines
"""

import os
import sys

from facio.pipeline.python.setup import Setup
from facio.pipeline.python.virtualenv import Virtualenv, run as venv_run
from mock import patch, PropertyMock

from .. import BaseTestCase


class TestPythonVirtualenv(BaseTestCase):

    def setUp(self):
        self._patch_clint([
            'facio.base.puts',
            'facio.pipeline.python.virtualenv.Virtualenv.warning',
            'facio.pipeline.python.virtualenv.Virtualenv.error',
        ])

        # Mocking State
        patcher = patch('facio.state.state.state',
                        new_callable=PropertyMock,
                        create=True)
        self.mock_state = patcher.start()
        self.mock_state.project_name = 'foo'
        self.mock_state.context_variables = {
            'PROJECT_NAME': 'foo'}
        self.addCleanup(patcher.stop)

    @patch('facio.base.input')
    def test_get_name(self, mock_input):
        mock_input.return_value = 'bar'

        i = Virtualenv()
        name = i.get_name()

        self.assertEqual(name, 'bar')

    @patch('facio.base.input')
    def test_get_name_default(self, mock_input):
        mock_input.return_value = ''

        i = Virtualenv()
        name = i.get_name()

        self.assertEqual(name, 'foo')

    @patch('facio.base.input')
    @patch('facio.pipeline.python.virtualenv.Virtualenv.get_name', create=True)
    def test_get_path(self, mock_get_name, mock_input):
        mock_get_name.return_value = 'baz'
        mock_input.return_value = '/foo/bar'

        i = Virtualenv()
        path = i.get_path()

        self.assertEqual(path, '/foo/bar/baz')

    @patch('facio.base.input')
    @patch('facio.pipeline.python.virtualenv.Virtualenv.get_name', create=True)
    def test_get_path_default(self, mock_get_name, mock_input):
        mock_get_name.return_value = 'baz'
        mock_input.return_value = ''
        user_dir = os.path.expanduser('~')

        i = Virtualenv()
        path = i.get_path()

        self.assertEqual(path, os.path.join(user_dir, '.virtualenvs', 'baz'))

    @patch('sh.virtualenv')
    @patch('facio.base.input')
    @patch('facio.pipeline.python.virtualenv.Virtualenv.get_path', create=True)
    def test_create(self, mock_get_path, mock_input, mock_virtualenv):
        mock_get_path.return_value = '/foo/bar/baz'
        mock_input.return_value = ''

        i = Virtualenv()
        path = i.create()

        mock_virtualenv.assert_called_with('/foo/bar/baz',
                                           '--no-site-packages')
        self.assertEqual(path, '/foo/bar/baz')

    @patch('sh.Environment.__getitem__', side_effect=ImportError)
    def test_create_import_error(self, mock_sh_import):
        mock_sh_import.side_effect = ImportError

        i = Virtualenv()
        path = i.create()
        warn = self.mocked_facio_pipeline_python_virtualenv_Virtualenv_warning

        self.assertEqual(path, None)
        warn.assert_called_with("Please install virtualenv to use the "
                                "python virtualenv pipeline")

    @patch('sh.virtualenv')
    @patch('facio.base.input')
    @patch('facio.pipeline.python.virtualenv.Virtualenv.get_path', create=True)
    def test_create_venv_exception(self, mock_get_path, mock_input,
                                   mock_virtualenv):
        mock_get_path.return_value = '/foo/bar/baz'
        mock_virtualenv.side_effect = Exception

        i = Virtualenv()
        path = i.create()
        err = self.mocked_facio_pipeline_python_virtualenv_Virtualenv_error

        self.assertEqual(path, None)
        err.assert_called_with("Failed to create virtual "
                               "environment at: /foo/bar/baz")

    @patch('sh.virtualenv')
    @patch('facio.base.input')
    @patch('facio.pipeline.python.virtualenv.Virtualenv.get_path', create=True)
    def test_run(self, mock_get_path, mock_input, mock_virtualenv):
        mock_get_path.return_value = '/foo/bar/baz'
        mock_input.return_value = 'n'

        path = venv_run()

        self.assertEqual(path, '/foo/bar/baz')


class TestSetup(BaseTestCase):

    def setUp(self):
        self._patch_clint([
            'facio.base.puts',
            'facio.pipeline.python.setup.Setup.warning',
            'facio.pipeline.python.setup.Setup.error',
        ])

        # Mocking State
        patcher = patch('facio.state.state.state',
                        new_callable=PropertyMock,
                        create=True)
        self.mock_state = patcher.start()
        self.mock_state.project_name = 'foo'
        self.mock_state.context_variables = {
            'PROJECT_NAME': 'foo'}
        self.addCleanup(patcher.stop)

    @patch('facio.base.input')
    def test_get_install_arg(self, mock_input):
        mock_input.return_value = 'develop'

        i = Setup()
        arg = i.get_install_arg()

        self.assertEqual(arg, 'develop')

    @patch('facio.base.input')
    def test_get_install_arg_input_error(self, mock_input):
        mock_input.return_value = 'foo'

        i = Setup()
        arg = i.get_install_arg()
        e = self.mocked_facio_pipeline_python_setup_Setup_error

        self.assertEqual(arg, None)
        e.assert_called_with("You did not enter a valid setup.py arg")

    def test_get_default_python_path_current(self):
        i = Setup()
        path = i.get_default_path_to_python()

        self.assertEqual(sys.executable, path)

    def test_get_default_path_virtualenv(self):
        self.mock_state.pipeline_calls = [(
            'facio.pipeline.python.virtualenv', '/foo/bar/python'
        )]

        i = Setup()
        path = i.get_default_path_to_python()

        self.assertEqual('/foo/bar/python', path)

    @patch('facio.pipeline.python.setup.Setup.get_default_path_to_python')
    @patch('facio.base.input')
    def test_get_python_path_default(self, mock_input, mock_default):
        mock_input.return_value = ''
        mock_default.return_value = '/foo/bar/python'

        i = Setup()
        path = i.get_path_to_python()

        self.assertEqual(path, '/foo/bar/python')

    @patch('facio.base.input')
    def test_get_python_path_input(self, mock_input):
        mock_input.return_value = '/foo/bar/python'

        i = Setup()
        path = i.get_path_to_python()

        self.assertEqual(path, '/foo/bar/python')
