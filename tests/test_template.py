# -*- coding: utf-8 -*-

"""
.. module:: tests.template
   :synopsis: Unit tests for template module
"""

from facio.exceptions import FacioException
from facio.template import Template
from mock import MagicMock, patch
from shutil import Error as ShutilError

from . import BaseTestCase


class TemplateTests(BaseTestCase):
    """ Template Tests """

    def setUp(self):
        self._patch_clint([
            'facio.base.puts',
            'facio.exceptions.puts',
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

        try:
            instance.copy()
        except:
            pass  # We don't care

        mock_gitvcs.assert_called_with('git+/foo/bar')



#import os
#import tempfile
#import uuid
#
#from codecs import open
#from facio.template import Template
#from mock import MagicMock, PropertyMock, patch
#from shutil import rmtree
#
#from . import BaseTestCase
#
#
#class TemplateTests(BaseTestCase):
#    """ Template Tests """
#
#    def setUp(self):
#        self.clint_paths = [
#            'facio.template.puts',
#        ]
#        self._mock_clint_start()
#        self.config = MagicMock(name='config')
#        self.config.project_name = uuid.uuid4().hex  # Random project name
#        self.config.django_secret_key = 'xxx'
#        self.config.template_settings_dir = 'settings'
#        self.config.cli_opts.error = MagicMock(side_effect=Exception)
#        self.config.template = os.path.join(os.path.dirname(
#            os.path.realpath(__file__)), 'files', 'template')
#        self.config._tpl = self.config.template
#
#    def test_handle_malformed_variables_gracefully(self):
#        self.config.variables = 'this,is.wrong'
#        t = Template(self.config)
#
#        self.assertEquals(len(t.place_holders), 3)
#
#    def test_custom_variables_added_to_placeholders(self):
#        self.config.variables = 'foo=bar,baz=1'
#        t = Template(self.config)
#
#        self.assertTrue('foo' in t.place_holders)
#        self.assertEquals(t.place_holders['foo'], 'bar')
#        self.assertTrue('baz' in t.place_holders)
#        self.assertEquals(t.place_holders['baz'], '1')
#
#    @patch('facio.template.Template.has_pipeline_file',
#           new_callable=PropertyMock,
#           return_value=False)
#    @patch('os.path.isdir', return_value=True)
#    @patch('facio.config.Config._error')
#    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
#    def test_dir_cannot_be_created_if_already_exists(self, mock_working_dir,
#                                                     mock_error, mock_isdir,
#                                                     mock_pipeline_file):
#        mock_working_dir.return_value = tempfile.gettempdir()
#        tmp_dir = tempfile.mkdtemp(suffix=self.config.project_name, prefix='')
#        tmp_dir_name = list(os.path.split(tmp_dir))[-1:][0]
#        self.config.project_name = tmp_dir_name
#        t = Template(self.config)
#        t.copy_template()
#        rmtree(tmp_dir)
#
#        self.config._error.assert_called_with('%s already exists' % (tmp_dir))
#
#    @patch('facio.template.Template.has_pipeline_file',
#           new_callable=PropertyMock,
#           return_value=False)
#    @patch('os.mkdir', return_value=True)
#    @patch('facio.config.Config._error')
#    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
#    def test_exception_if_directory_creation_fails(self, mock_working_dir,
#                                                   mock_error,
#                                                   mock_os_mkdir,
#                                                   mock_pipeline_file):
#        mock_working_dir.return_value = tempfile.gettempdir()
#        tmp_dir = tempfile.mkdtemp(suffix=self.config.project_name, prefix='')
#        tmp_dir_name = list(os.path.split(tmp_dir))[-1:][0]
#        self.config.project_name = tmp_dir_name
#        t = Template(self.config)
#        t.copy_template()
#
#        self.config._error.assert_called_with(
#            'Error creating project directory')
#        mock_os_mkdir.assert_called_with(os.path.join(
#            t.working_dir, self.config.project_name))
#
#    @patch('tempfile.mkdtemp', return_value=True)
#    @patch('facio.vcs.git.Git.clone', return_value=True)
#    @patch('facio.vcs.git.Git.tmp_dir', return_value=True)
#    def test_detect_git_repo(self, mock_tmp_dir, mock_clone, mock_tempfile):
#        t = Template(self.config)
#        assert not t.vcs_cls
#        self.config.template = 'git+git@somewhere.com:repo.git'
#        t = Template(self.config)
#        self.assertEquals(t.vcs_cls.__class__.__name__, 'Git')
#
#    @patch('tempfile.mkdtemp', return_value=True)
#    @patch('facio.vcs.hg.Mercurial.clone', return_value=True)
#    @patch('facio.vcs.hg.Mercurial.tmp_dir', return_value=True)
#    def test_detect_hg_repo(self, mock_tmp_dir, mock_clone, mock_tempfile):
#        t = Template(self.config)
#        assert not t.vcs_cls
#        self.config.template = 'hg+ssh://someone@somewhere.com//path'
#        t = Template(self.config)
#        self.assertEquals(t.vcs_cls.__class__.__name__, 'Mercurial')
#
#    @patch('facio.template.Template.has_pipeline_file',
#           new_callable=PropertyMock,
#           return_value=False)
#    @patch('os.path.isdir', return_value=False)
#    @patch('facio.config.Config._error')
#    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
#    def test_copy_template_failes_if_dir_does_not_exist(
#            self, mock_working_dir, mock_error, mock_isdir,
#            mock_pipeline_file):
#        mock_working_dir.return_value = tempfile.gettempdir()
#        tmp_dir = tempfile.mkdtemp(suffix=self.config.project_name, prefix='')
#        tmp_dir_name = list(os.path.split(tmp_dir))[-1:][0]
#        self.config.project_name = tmp_dir_name
#        t = Template(self.config)
#        t.copy_template()
#        self.config._error.assert_called_with(
#            'Unable to copy template, directory does not exist')
#
#    @patch('facio.template.Template.has_pipeline_file',
#           new_callable=PropertyMock,
#           return_value=False)
#    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
#    def test_excluded_dirs_are_not_copied(self, mock_working_dir,
#                                          mock_has_pipeline):
#        mock_working_dir.return_value = tempfile.gettempdir()
#        t = Template(self.config)
#        t.exclude_dirs.append('.exclude_this')
#        t.copy_template()
#        self.assertFalse(os.path.isdir(os.path.join(t.project_root,
#                                                    '.exclude_this')))
#        rmtree(t.project_root)
#
#    @patch('facio.template.Template.has_pipeline_file',
#           new_callable=PropertyMock,
#           return_value=False)
#    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
#    def test_copy_directory_tree_if_is_dir(self, mock_working_dir,
#                                           mock_pipeline_file):
#        mock_working_dir.return_value = tempfile.gettempdir()
#        t = Template(self.config)
#        t.exclude_dirs.append('.exclude_this')
#        t.copy_template()
#        self.assertTrue(os.path.isdir(os.path.join(t.project_root,
#                                                   'should_copy_this')))
#        rmtree(t.project_root)
#
#    @patch('facio.template.Template.has_pipeline_file',
#           new_callable=PropertyMock,
#           return_value=False)
#    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
#    def test_directory_not_renamed_if_not_in_placeholders(self,
#                                                          mock_working_dir,
#                                                          mock_pipeline_file):
#        mock_working_dir.return_value = tempfile.gettempdir()
#        t = Template(self.config)
#        t.copy_template()
#        self.assertTrue(os.path.isdir(os.path.join(t.project_root,
#                                                   '{{NOT_IN_PLACEHOLDERS}}'))
#                                                    )
#        rmtree(t.project_root)
#
#    @patch('facio.template.Template.has_pipeline_file',
#           new_callable=PropertyMock,
#           return_value=False)
#    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
#    def test_rename_files_in_placeholders(self, mock_working_dir,
#                                          mock_pipeline_file):
#        mock_working_dir.return_value = tempfile.gettempdir()
#        t = Template(self.config)
#        t.copy_template()
#        self.assertTrue(os.path.isfile(os.path.join(
#            t.project_root, '{{NOT_IN_PLACEHOLDERS}}',
#            '%s.txt' % self.config.project_name)))
#        rmtree(t.project_root)
#
#    @patch('facio.template.Template.has_pipeline_file',
#           new_callable=PropertyMock,
#           return_value=False)
#    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
#    def test_files_are_ignores(self, mock_working_dir, mock_pipeline_file):
#        mock_working_dir.return_value = tempfile.gettempdir()
#        self.config.ignore = ['*.gif', '*.png', 'i_dont_need_processing.txt']
#        t = Template(self.config)
#        t.copy_template()
#        should_ignore = [
#            'ignore.gif',
#            'ignore.png',
#            'i_dont_need_processing.txt'
#        ]
#        for root, dirs, files in os.walk(t.project_root):
#            for name in files:
#                if name in should_ignore:
#                    filepath = os.path.join(root, name)
#                    with open(filepath, 'r', encoding='utf8') as f:
#                        contents = f.read()
#                    self.assertEqual(contents, '{{ PROJECT_NAME }}\n')
#
#    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
#    def test_detects_pipeline_file(self, mock_working_dir):
#        mock_working_dir.return_value = tempfile.gettempdir()
#        t = Template(self.config)
#        self.assertTrue(t.has_pipeline_file)
#        self.assertEqual(
#            t.pipeline_file,
#            os.path.join(t.config._tpl, '.facio.pipeline.yml'))
#
#    @patch('os.path.isfile', return_value=False)
#    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
#    def test_false_no_pipeline_file(self, mock_working_dir, mock_isfile):
#        mock_working_dir.return_value = tempfile.gettempdir()
#        t = Template(self.config)
#        self.assertFalse(t.has_pipeline_file)
#        self.assertFalse(hasattr(t, 'pipeline_file'))
#
#    @patch('facio.pipeline.Pipeline.run_before')
#    @patch('facio.pipeline.Pipeline.run_after')
#    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
#    def test_runs_pipelines(self, mock_working_dir, mock_after, mock_before):
#        mock_working_dir.return_value = tempfile.gettempdir()
#        t = Template(self.config)
#        t.copy_template()
#        self.assertTrue(mock_before.called)
#        self.assertTrue(mock_after.called)
