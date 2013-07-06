# -*- coding: utf-8 -*-

"""
.. module:: tests.template
   :synopsis: Unit tests for template module
"""

from facio.exceptions import FacioException
from facio.template import Template
from mock import MagicMock, mock_open, patch
from shutil import Error as ShutilError
from six import iteritems

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

    def test_path_and_name_set(self):
        instance = Template('foo', '/foo/bar')

        self.assertEqual(instance.name, 'foo')
        self.assertEqual(instance.path, '/foo/bar')

    @patch('facio.template.pwd', return_value='/foo')
    def test_return_current_working_dir(self, mock_pwd):
        instance = Template('foo', '/foo/bar')

        self.assertEqual(instance.get_working_directory(), '/foo')

    @patch('facio.template.pwd', return_value='/bar')
    def test_return_project_root(self, mock_pwd):
        instance = Template('foo', '/foo/bar')

        self.assertEqual(instance.get_project_root(), '/bar/foo')

    @patch('sys.exit')
    def test_update_context_variables_must_take_dict(self, mock_exit):
        instance = Template('foo', '/foo/bar')

        with self.assertRaises(FacioException):
            instance.update_context_variables([1, 2, 3])
        self.assertTrue(mock_exit.called)
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: Variable update failed')

    @patch('facio.template.Template.__init__', return_value=None)
    def test_get_context_variables_empty(self, mock_init):
        instance = Template('foo', '/foo/bar')

        self.assertEqual(instance.get_context_variables(), {})

    def test_get_context_variables(self):
        instance = Template('foo', '/foo/bar')

        self.assertEqual(instance.get_context_variables(), {
            'PROJECT_NAME': 'foo'})

    def test_get_context_variable(self):
        instance = Template('foo', '/foo/bar')

        self.assertEqual(instance.get_context_variable('PROJECT_NAME'), 'foo')
        self.assertFalse(instance.get_context_variable('not_created'), 'foo')

    def test_update_ignore_globs_empty_wrong_type(self):
        instance = Template('foo', '/foo/bar')
        del(instance.ignore_globs)

        instance.update_ignore_globs({'foo': 'bar'})

        self.assertEqual(instance.ignore_globs, [])

    @patch('sys.exit')
    def test_exception_setting_ignore_globs_not_iterable(self, mock_exit):
        instance = Template('foo', '/foo/bar')

        with self.assertRaises(FacioException):
            instance.update_ignore_globs(1)
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: Failed to add 1 to ignore globs list')
        self.assertTrue(mock_exit.called)

    def test_get_ignore_globs_empty_list(self):
        instance = Template('foo', '/foo/bar')
        del(instance.ignore_globs)

        self.assertEqual(instance.get_ignore_globs(), [])

    def test_get_ignore_globs(self):
        instance = Template('foo', '/foo/bar')
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
        instance = Template('foo', '/foo/bar')
        instance.update_ignore_globs(['*.png', '*.gif'])
        files = ['setup.py', 'setup.pyc', 'foo.png', '.git', 'index.html']

        ignores = instance.get_ignore_files(files)

        self.assertEqual(ignores, ['.git', 'setup.pyc', 'foo.png'])

    @patch('sys.exit')
    @patch('facio.template.pwd', return_value='/tmp')
    @patch('facio.template.shutil.copytree', side_effect=ShutilError)
    def test_copy_shutil_error_raise_exception(
            self,
            mock_copy_tree,
            mock_pwd,
            mock_exit):

        instance = Template('foo', '/foo/bar')

        with self.assertRaises(FacioException):
            instance.copy()
        self.assertTrue(mock_exit.called)
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: Failed to copy /foo/bar to /tmp/foo')

    @patch('sys.exit')
    @patch('facio.template.os.path.isdir', return_value=True)
    @patch('facio.template.pwd', return_value='/tmp')
    @patch('facio.template.shutil.copytree', side_effect=OSError)
    def test_copy_shutil_oserror_raise_exception(
            self,
            mock_copy_tree,
            mock_pwd,
            mock_isdir,
            mock_exit):

        instance = Template('foo', '/foo/bar')

        with self.assertRaises(FacioException):
            instance.copy()
        mock_isdir.assert_called_with('/tmp/foo')
        self.assertTrue(mock_exit.called)
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: /tmp/foo already exists')

    @patch('sys.exit')
    @patch('facio.template.os.path.isdir', return_value=False)
    @patch('facio.template.pwd', return_value='/tmp')
    @patch('facio.template.shutil.copytree', side_effect=OSError)
    def test_copy_oserror_not_vcs_path_exception(
            self,
            mock_copy_tree,
            mock_pwd,
            mock_isdir,
            mock_exit):

        instance = Template('foo', '/foo/bar')

        with self.assertRaises(FacioException):
            instance.copy()
        mock_isdir.assert_called_with('/tmp/foo')
        self.assertTrue(mock_exit.called)
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: /foo/bar does not exist')

    @patch('sys.exit')
    @patch('facio.template.GitVCS', new_callable=MagicMock)
    @patch('facio.template.os.path.isdir', return_value=False)
    @patch('facio.template.pwd', return_value='/tmp')
    @patch('facio.template.shutil.copytree', side_effect=OSError)
    def test_copy_oserror_vcs_path(
            self,
            mock_copy_tree,
            mock_pwd,
            mock_isdir,
            mock_gitvcs,
            mock_exit):

        instance = Template('foo', 'git+/foo/bar')
        instance.COPY_ATTEMPT_LIMIT = 0  # Block the next copy call

        with self.assertRaises(FacioException):
            instance.copy()
        mock_gitvcs.assert_called_with('git+/foo/bar')

    @patch('sys.exit')
    @patch('facio.template.GitVCS', new_callable=MagicMock)
    @patch('facio.template.os.path.isdir', return_value=False)
    @patch('facio.template.pwd', return_value='/tmp')
    @patch('facio.template.shutil.copytree', side_effect=OSError)
    def test_copy_oserror_vcs_path_recursion_limit(
            self,
            mock_copy_tree,
            mock_pwd,
            mock_isdir,
            mock_gitvcs,
            mock_exit):

        instance = Template('foo', 'git+/foo/bar')
        with self.assertRaises(FacioException):
            instance.copy()
        self.assertTrue(mock_exit.called)
        self.mocked_facio_exceptions_puts.assert_any_call(
            'Error: Failed to copy template after 6 attempts')

    @patch('facio.template.shutil.copytree', new_callable=MagicMock)
    def test_copy_returns_true(self, mock_copy_tree):
        instance = Template('foo', '/foo/bar')

        self.assertTrue(instance.copy())

    @patch('os.walk')
    @patch('facio.template.shutil.move', new_callable=MagicMock)
    def test_rename_directories(self, mock_move, mock_walk):
        mock_walk.return_value = [
            ('/foo', ['bar', '{{UNKNOWN}}', '{{PROJECT_NAME}}', 'baz'], [])
        ]
        instance = Template('foo', '/foo/bar')

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
        instance = Template('foo', '/foo/bar')

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

        instance = Template('foo', '/foo/bar')
        instance.rename()

        self.assertEqual(self.mocked_facio_template_Template_out.call_count, 2)
        self.mocked_facio_template_Template_out.has_any_call(
            'Renaming /foo/{{PROJECT_NAME}} to /foo/foo')
        self.mocked_facio_template_Template_out.has_any_call(
            'Renaming /foo/{{PROJECT_NAME}}.png to /foo/foo.png')

    @patch('os.walk')
    @patch('facio.template.FileSystemLoader.get_source')
    def test_write(self, mock_get_source, mock_walk):

        # Mock Setups - Fake file contents and open writer
        files_map = {
            'bar.py': '{{PROJECT_NAME}}',
            'foo.png': 'PNGIHDRÄIDATxÚcøûýhúÌIEND®B`',
            'baz.html': '<h1>{{UNKNOWN|default(\'Hello World\')}}</h1>',
            'baz.gif': 'I am a gif'
        }

        def get_source(environmet, template):
            """ Overriding Jinja2 FileSystemLoader get_source
            function so we can return our own source. """

            contents = files_map[template]
            return contents.decode(), template, True

        mock_get_source.side_effect = get_source
        mock_walk.return_value = [
            ('/foo', [], [k for k, v in iteritems(files_map)])
        ]

        open_mock = mock_open()
        open_patcher = patch('facio.template.open', open_mock, create=True)
        open_patcher.start()

        # Call the write method on facio.Template
        instance = Template('foo', '/foo/bar')
        instance.update_ignore_globs(['*.gif', ])
        instance.write()

        # Assertions
        handle = open_mock()
        self.assertEqual(handle.write.call_count, 2)
        handle.write.assert_any_call('foo')
        handle.write.assert_any_call('<h1>Hello World</h1>')
        self.mocked_facio_template_Template_warning.assert_called_with(
            'Failed to render /foo/foo.png: \'ascii\' codec can\'t decode '
            'byte 0xc2 in position 0: ordinal not in range(128)')

        # Stop the open patch
        open_patcher.stop()
