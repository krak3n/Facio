# -*- coding: utf-8 -*-

"""
.. module:: tests.template
   :synopsis: Unit tests for template module
"""

import six

from facio.exceptions import FacioException
from facio.template import Template
from mock import MagicMock, mock_open, PropertyMock, patch
from shutil import Error as ShutilError

from . import BaseTestCase


class TemplateTests(BaseTestCase):
    """ Template Tests """

    def setUp(self):
        self._patch_clint([
            'facio.base.puts',
            'facio.exceptions.puts',
            'facio.template.Template.out',
            'facio.template.Template.warning',
        ])

        # Temp Directory Patch
        patcher = patch('facio.vcs.tempfile.mkdtemp',
                        return_vale='/tmp/tmpAGmDfZfacio')
        patcher.start()
        self.addCleanup(patcher.stop)

        # Mocking State
        patcher = patch('facio.template.state.state',
                        new_callable=PropertyMock,
                        create=True)
        self.mock_state = patcher.start()
        self.mock_state.project_name = 'foo'
        self.mock_state.context_variables = {
            'PROJECT_NAME': 'foo'}
        self.addCleanup(patcher.stop)

    def test_set_origin(self):
        instance = Template('/foo/bar')

        self.assertEqual(instance.origin, '/foo/bar')

    def test_update_ignore_globs_empty_wrong_type(self):
        instance = Template('/foo/bar')
        del(instance.ignore_globs)

        instance.update_ignore_globs({'foo': 'bar'})

        self.assertEqual(instance.ignore_globs, [])

    @patch('sys.exit')
    def test_exception_setting_ignore_globs_not_iterable(self, mock_exit):
        instance = Template('/foo/bar')

        with self.assertRaises(FacioException):
            instance.update_ignore_globs(1)
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: Failed to add 1 to ignore globs list')
        self.assertTrue(mock_exit.called)

    def test_get_ignore_globs_empty_list(self):
        instance = Template('/foo/bar')
        del(instance.ignore_globs)

        self.assertEqual(instance.get_ignore_globs(), [])

    def test_get_ignore_globs(self):
        instance = Template('/foo/bar')
        instance.update_ignore_globs(['*.png', '*.gif'])

        self.assertEqual(instance.get_ignore_globs(), [
            '.git',
            '.hg',
            '.svn',
            '*.pyc',
            '*.png',
            '*.gif'
        ])

    def test_get_ignore_files(self):
        instance = Template('/foo/bar')
        instance.update_ignore_globs(['*.png', '*.gif'])
        files = ['setup.py', 'setup.pyc', 'foo.png', '.git', 'index.html']

        ignores = instance.get_ignore_files(files)

        self.assertEqual(ignores, ['.git', 'setup.pyc', 'foo.png'])

    @patch('sys.exit')
    @patch('facio.state.pwd', return_value='/tmp')
    @patch('facio.template.shutil.copytree', side_effect=ShutilError)
    def test_copy_shutil_error_raise_exception(
            self,
            mock_copy_tree,
            mock_pwd,
            mock_exit):

        instance = Template('/foo/bar')

        with self.assertRaises(FacioException):
            instance.copy()
        self.assertTrue(mock_exit.called)
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: Failed to copy /foo/bar to /tmp/foo')

    @patch('sys.exit')
    @patch('facio.state.pwd', return_value='/tmp')
    @patch('facio.template.os.path.isdir', return_value=True)
    @patch('facio.template.shutil.copytree', side_effect=OSError)
    def test_copy_shutil_oserror_raise_exception(
            self,
            mock_copy_tree,
            mock_isdir,
            mock_pwd,
            mock_exit):

        instance = Template('/foo/bar')

        with self.assertRaises(FacioException):
            instance.copy()
        mock_isdir.assert_called_with('/tmp/foo')
        self.assertTrue(mock_exit.called)
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: /tmp/foo already exists')

    @patch('sys.exit')
    @patch('facio.state.pwd', return_value='/tmp')
    @patch('facio.template.os.path.isdir', return_value=False)
    @patch('facio.template.shutil.copytree', side_effect=OSError)
    def test_copy_oserror_not_vcs_path_exception(
            self,
            mock_copy_tree,
            mock_isdir,
            mock_pwd,
            mock_exit):

        instance = Template('/foo/bar')

        with self.assertRaises(FacioException):
            instance.copy()
        mock_isdir.assert_called_with('/tmp/foo')
        self.assertTrue(mock_exit.called)
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: /foo/bar does not exist')

    @patch('sys.exit')
    @patch('facio.template.GitVCS', new_callable=MagicMock)
    @patch('facio.template.os.path.isdir', return_value=False)
    @patch('facio.template.shutil.copytree', side_effect=OSError)
    def test_copy_oserror_vcs_path(
            self,
            mock_copy_tree,
            mock_isdir,
            mock_gitvcs,
            mock_exit):

        instance = Template('git+/foo/bar')
        instance.COPY_ATTEMPT_LIMIT = 0  # Block the next copy call

        with self.assertRaises(FacioException):
            instance.copy()
        mock_gitvcs.assert_called_with('git+/foo/bar')

    @patch('sys.exit')
    @patch('facio.template.GitVCS.clone', return_value=False)
    @patch('facio.template.os.path.isdir', return_value=False)
    @patch('facio.template.shutil.copytree', side_effect=OSError)
    def test_copy_oserror_vcs_clone_returns_not_path(
            self,
            mock_copy_tree,
            mock_isdir,
            mock_gitvcs,
            mock_exit):

        instance = Template('git+/foo/bar')
        instance.COPY_ATTEMPT_LIMIT = 0  # Block the next copy call

        with self.assertRaises(FacioException):
            instance.copy()
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: New path to template not returned by GitVCS.clone()')

    @patch('sys.exit')
    @patch('facio.template.GitVCS', new_callable=MagicMock)
    @patch('facio.template.os.path.isdir', return_value=False)
    @patch('facio.template.shutil.copytree', side_effect=OSError)
    def test_copy_oserror_vcs_path_recursion_limit(
            self,
            mock_copy_tree,
            mock_isdir,
            mock_gitvcs,
            mock_exit):

        instance = Template('git+/foo/bar')
        with self.assertRaises(FacioException):
            instance.copy()
        self.assertTrue(mock_exit.called)
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: Failed to copy template after 6 attempts')

    @patch('facio.template.shutil.copytree', new_callable=MagicMock)
    def test_copy_returns_true(self, mock_copy_tree):
        instance = Template('/foo/bar')

        self.assertTrue(instance.copy())

    @patch('facio.state.pwd', return_value='/tmp')
    @patch('facio.template.shutil.copytree', new_callable=MagicMock)
    def test_copy_callback_call(self, mock_copy_tree, mock_pwd):
        from facio.state import state
        instance = Template('/foo/bar')
        callback = MagicMock()

        self.assertTrue(instance.copy(callback=callback))
        callback.assert_called_once_with(
            origin=instance.origin,
            destination=state.get_project_root())

    @patch('os.walk')
    @patch('facio.template.shutil.move', new_callable=MagicMock)
    def test_rename_directories(self, mock_move, mock_walk):
        mock_walk.return_value = [
            ('/foo', ['bar', '{{UNKNOWN}}', '{{PROJECT_NAME}}', 'baz'], [])
        ]
        instance = Template('/foo/bar')

        for index, value in enumerate(instance.rename_direcories()):
            old, new = value
            mock_move.assert_called_with(old, new)
            self.assertEqual(old, '/foo/{{PROJECT_NAME}}')
            self.assertEqual(new, '/foo/foo')

    @patch('os.walk')
    @patch('facio.template.shutil.move', new_callable=MagicMock)
    def test_rename_files(self, mock_move, mock_walk):
        mock_walk.return_value = [
            ('/foo', [], ['bar.py', '{{UNKNOWN}}.png',
                          '{{PROJECT_NAME}}.html', 'baz.gif'])
        ]
        instance = Template('/foo/bar')

        for index, value in enumerate(instance.rename_files()):
            old, new = value
            mock_move.assert_called_with(old, new)
            self.assertEqual(old, '/foo/{{PROJECT_NAME}}.html')
            self.assertEqual(new, '/foo/foo.html')

    @patch('os.walk')
    @patch('facio.template.shutil.move', new_callable=MagicMock)
    def test_rename(self, mock_move, mock_walk):
        mock_walk.return_value = [(
            '/foo',  # Root
            ['{{PROJECT_NAME}}', 'baz'],  # Dirs
            ['bar.py', '{{PROJECT_NAME}}.png', 'baz.gif'],  # Files
        )]

        instance = Template('/foo/bar')
        instance.rename()

        self.assertEqual(self.mocked_facio_template_Template_out.call_count, 2)
        self.mocked_facio_template_Template_out.has_any_call(
            'Renaming /foo/{{PROJECT_NAME}} to /foo/foo')
        self.mocked_facio_template_Template_out.has_any_call(
            'Renaming /foo/{{PROJECT_NAME}}.png to /foo/foo.png')

    @patch('os.walk')
    @patch('facio.template.FileSystemLoader.get_source')
    def test_render(self, mock_get_source, mock_walk):

        # Mock Setups - Fake file contents and open renderer
        files_map = {
            'bar.py': '{{PROJECT_NAME}}',
            'foo.png': 'PNGIHDRÄIDATxÚcøûýhúÌIEND®B`',
            'baz.html': '<h1>{{UNKNOWN|default(\'Hello World\')}}</h1>',
            'baz.gif': 'I am a gif'
        }

        def get_source(environmet, template):
            """ Overriding Jinja2 FileSystemLoader get_source
            function so we can return our own source. """

            if template == 'foo.png':
                raise Exception('\'utf8\' codec can\'t decode byte '
                                '0x89 in position 0: invalid start '
                                'byte')

            contents = files_map[template]
            return contents, template, True

        mock_get_source.side_effect = get_source
        mock_walk.return_value = [
            ('/foo', [], [k for k, v in six.iteritems(files_map)])
        ]

        open_mock = mock_open()
        open_patcher = patch('facio.template.open', open_mock, create=True)
        open_patcher.start()

        # Call the renderer method on facio.Template
        instance = Template('/foo/bar')
        instance.update_ignore_globs(['*.gif', ])
        instance.render()

        # Assertions
        handle = open_mock()
        self.assertEqual(handle.write.call_count, 2)
        handle.write.assert_any_call('foo')
        handle.write.assert_any_call('<h1>Hello World</h1>')
        self.mocked_facio_template_Template_warning.assert_called_with(
            'Failed to render /foo/foo.png: \'utf8\' codec can\'t '
            'decode byte 0x89 in position 0: invalid start byte')

        # Stop the open patch
        open_patcher.stop()
