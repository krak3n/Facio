"""
.. module:: tests.template
   :synopsis: Unit tests for template module
"""

import os
import tempfile
import uuid

from codecs import open
from facio.template import Template
from mock import MagicMock, PropertyMock, patch
from shutil import rmtree

from .base import BaseTestCase


class TemplateTests(BaseTestCase):
    """ Template Tests """

    def setUp(self):
        self.clint_paths = [
            'facio.template.puts',
        ]
        self._mock_clint_start()
        self.config = MagicMock(name='config')
        self.config.project_name = uuid.uuid4().hex  # Random project name
        self.config.django_secret_key = 'xxx'
        self.config.template_settings_dir = 'settings'
        self.config.cli_opts.error = MagicMock(side_effect=Exception)
        self.config.template = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'files', 'template')
        self.config._tpl = self.config.template

    def test_handle_malformed_variables_gracefully(self):
        self.config.variables = 'this,is.wrong'
        t = Template(self.config)

        self.assertEquals(len(t.place_holders), 3)

    def test_custom_variables_added_to_placeholders(self):
        self.config.variables = 'foo=bar,baz=1'
        t = Template(self.config)

        self.assertTrue('foo' in t.place_holders)
        self.assertEquals(t.place_holders['foo'], 'bar')
        self.assertTrue('baz' in t.place_holders)
        self.assertEquals(t.place_holders['baz'], '1')

    @patch('facio.template.Template.has_pipeline_file',
           new_callable=PropertyMock,
           return_value=False)
    @patch('os.path.isdir', return_value=True)
    @patch('facio.config.Config._error')
    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_dir_cannot_be_created_if_already_exists(self, mock_working_dir,
                                                     mock_error, mock_isdir,
                                                     mock_pipeline_file):
        mock_working_dir.return_value = tempfile.gettempdir()
        tmp_dir = tempfile.mkdtemp(suffix=self.config.project_name, prefix='')
        tmp_dir_name = list(os.path.split(tmp_dir))[-1:][0]
        self.config.project_name = tmp_dir_name
        t = Template(self.config)
        t.copy_template()
        rmtree(tmp_dir)

        self.config._error.assert_called_with('%s already exists' % (tmp_dir))

    @patch('facio.template.Template.has_pipeline_file',
           new_callable=PropertyMock,
           return_value=False)
    @patch('os.mkdir', return_value=True)
    @patch('facio.config.Config._error')
    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_exception_if_directory_creation_fails(self, mock_working_dir,
                                                   mock_error,
                                                   mock_os_mkdir,
                                                   mock_pipeline_file):
        mock_working_dir.return_value = tempfile.gettempdir()
        tmp_dir = tempfile.mkdtemp(suffix=self.config.project_name, prefix='')
        tmp_dir_name = list(os.path.split(tmp_dir))[-1:][0]
        self.config.project_name = tmp_dir_name
        t = Template(self.config)
        t.copy_template()

        self.config._error.assert_called_with(
            'Error creating project directory')
        mock_os_mkdir.assert_called_with(os.path.join(
            t.working_dir, self.config.project_name))

    @patch('tempfile.mkdtemp', return_value=True)
    @patch('facio.vcs.git.Git.clone', return_value=True)
    @patch('facio.vcs.git.Git.tmp_dir', return_value=True)
    def test_detect_git_repo(self, mock_tmp_dir, mock_clone, mock_tempfile):
        t = Template(self.config)
        assert not t.vcs_cls
        self.config.template = 'git+git@somewhere.com:repo.git'
        t = Template(self.config)
        self.assertEquals(t.vcs_cls.__class__.__name__, 'Git')

    @patch('tempfile.mkdtemp', return_value=True)
    @patch('facio.vcs.hg.Mercurial.clone', return_value=True)
    @patch('facio.vcs.hg.Mercurial.tmp_dir', return_value=True)
    def test_detect_hg_repo(self, mock_tmp_dir, mock_clone, mock_tempfile):
        t = Template(self.config)
        assert not t.vcs_cls
        self.config.template = 'hg+ssh://someone@somewhere.com//path'
        t = Template(self.config)
        self.assertEquals(t.vcs_cls.__class__.__name__, 'Mercurial')

    @patch('facio.template.Template.has_pipeline_file',
           new_callable=PropertyMock,
           return_value=False)
    @patch('os.path.isdir', return_value=False)
    @patch('facio.config.Config._error')
    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_copy_template_failes_if_dir_does_not_exist(
            self, mock_working_dir, mock_error, mock_isdir,
            mock_pipeline_file):
        mock_working_dir.return_value = tempfile.gettempdir()
        tmp_dir = tempfile.mkdtemp(suffix=self.config.project_name, prefix='')
        tmp_dir_name = list(os.path.split(tmp_dir))[-1:][0]
        self.config.project_name = tmp_dir_name
        t = Template(self.config)
        t.copy_template()
        self.config._error.assert_called_with(
            'Unable to copy template, directory does not exist')

    @patch('facio.template.Template.has_pipeline_file',
           new_callable=PropertyMock,
           return_value=False)
    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_excluded_dirs_are_not_copied(self, mock_working_dir,
                                          mock_has_pipeline):
        mock_working_dir.return_value = tempfile.gettempdir()
        t = Template(self.config)
        t.exclude_dirs.append('.exclude_this')
        t.copy_template()
        self.assertFalse(os.path.isdir(os.path.join(t.project_root,
                                                    '.exclude_this')))
        rmtree(t.project_root)

    @patch('facio.template.Template.has_pipeline_file',
           new_callable=PropertyMock,
           return_value=False)
    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_copy_directory_tree_if_is_dir(self, mock_working_dir,
                                           mock_pipeline_file):
        mock_working_dir.return_value = tempfile.gettempdir()
        t = Template(self.config)
        t.exclude_dirs.append('.exclude_this')
        t.copy_template()
        self.assertTrue(os.path.isdir(os.path.join(t.project_root,
                                                   'should_copy_this')))
        rmtree(t.project_root)

    @patch('facio.template.Template.has_pipeline_file',
           new_callable=PropertyMock,
           return_value=False)
    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_directory_not_renamed_if_not_in_placeholders(self,
                                                          mock_working_dir,
                                                          mock_pipeline_file):
        mock_working_dir.return_value = tempfile.gettempdir()
        t = Template(self.config)
        t.copy_template()
        self.assertTrue(os.path.isdir(os.path.join(t.project_root,
                                                   '{{NOT_IN_PLACEHOLDERS}}')))
        rmtree(t.project_root)

    @patch('facio.template.Template.has_pipeline_file',
           new_callable=PropertyMock,
           return_value=False)
    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_rename_files_in_placeholders(self, mock_working_dir,
                                          mock_pipeline_file):
        mock_working_dir.return_value = tempfile.gettempdir()
        t = Template(self.config)
        t.copy_template()
        self.assertTrue(os.path.isfile(os.path.join(
            t.project_root, '{{NOT_IN_PLACEHOLDERS}}',
            '%s.txt' % self.config.project_name)))
        rmtree(t.project_root)

    @patch('facio.template.Template.has_pipeline_file',
           new_callable=PropertyMock,
           return_value=False)
    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_files_are_ignores(self, mock_working_dir, mock_pipeline_file):
        mock_working_dir.return_value = tempfile.gettempdir()
        self.config.ignore = ['*.gif', '*.png', 'i_dont_need_processing.txt']
        t = Template(self.config)
        t.copy_template()
        should_ignore = [
            'ignore.gif',
            'ignore.png',
            'i_dont_need_processing.txt'
        ]
        for root, dirs, files in os.walk(t.project_root):
            for name in files:
                if name in should_ignore:
                    filepath = os.path.join(root, name)
                    with open(filepath, 'r', encoding='utf8') as f:
                        contents = f.read()
                    self.assertEqual(contents, '{{ PROJECT_NAME }}\n')

    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_detects_pipeline_file(self, mock_working_dir):
        mock_working_dir.return_value = tempfile.gettempdir()
        t = Template(self.config)
        self.assertTrue(t.has_pipeline_file)
        self.assertEqual(
            t.pipeline_file,
            os.path.join(t.config._tpl, '.facio.pipeline.yml'))

    @patch('os.path.isfile', return_value=False)
    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_false_no_pipeline_file(self, mock_working_dir, mock_isfile):
        mock_working_dir.return_value = tempfile.gettempdir()
        t = Template(self.config)
        self.assertFalse(t.has_pipeline_file)
        self.assertFalse(hasattr(t, 'pipeline_file'))

    @patch('facio.pipeline.Pipeline.run_before')
    @patch('facio.pipeline.Pipeline.run_after')
    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_runs_pipelines(self, mock_working_dir, mock_after, mock_before):
        mock_working_dir.return_value = tempfile.gettempdir()
        t = Template(self.config)
        t.copy_template()
        self.assertTrue(mock_before.called)
        self.assertTrue(mock_after.called)
