import os
import tempfile
import unittest
import uuid

from mock import MagicMock, PropertyMock, patch
from facio.template import Template
from sh import git
from shutil import rmtree
from StringIO import StringIO


class TemplateTests(unittest.TestCase):
    """ Template Tests """

    def setUp(self):
        # Mock out the config class
        self.config = MagicMock(name='config')
        self.config.project_name = uuid.uuid4().hex  # Random project name
        self.config.django_secret_key = 'xxx'
        self.config.template_settings_dir = 'settings'
        self.config.cli_opts.error = MagicMock(side_effect=Exception)
        self.config.template = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'test_template')
        self.config._tpl = self.config.template
        self.puts_patch = patch('facio.template.puts',
                                stream=StringIO)
        self.puts_patch.start()
        self.puts_patch_vcs = patch('facio.vcs.git.puts',
                                    stream=StringIO)
        self.puts_patch_vcs.start()

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

    @patch('os.path.isdir', return_value=True)
    @patch('facio.config.Config._error')
    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_dir_cannot_be_created_if_already_exists(self, mock_working_dir,
                                                     mock_error, mock_isdir):
        mock_working_dir.return_value = tempfile.gettempdir()
        tmp_dir = tempfile.mkdtemp(suffix=self.config.project_name, prefix='')
        tmp_dir_name = list(os.path.split(tmp_dir))[-1:][0]
        self.config.project_name = tmp_dir_name
        t = Template(self.config)
        t.copy_template()
        rmtree(tmp_dir)

        self.config._error.assert_called_with('%s already exists' % (tmp_dir))

    @patch('os.mkdir', return_value=True)
    @patch('facio.config.Config._error')
    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_exception_if_directory_creation_fails(self, mock_working_dir,
                                                   mock_error,
                                                   mock_os_mkdir):
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

    @patch('sys.stdout', new_callable=StringIO)
    @patch('tempfile.mkdtemp', return_value=True)
    @patch('facio.vcs.git.Git.clone', return_value=True)
    @patch('facio.vcs.git.Git.tmp_dir', return_value=True)
    def test_detect_git_repo(self, mock_tmp_dir, mock_clone, mock_tempfile,
                             mock_stdout):
        t = Template(self.config)
        assert not t.vcs_cls
        self.config.template = 'git+git@somewhere.com:repo.git'
        t = Template(self.config)
        self.assertEquals(t.vcs_cls.__class__.__name__, 'Git')

    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_clone_git_repo(self, mock_working_dir):

        # Create a fake temp repo w/ commit
        git_dir = tempfile.mkdtemp(prefix='git')
        git.init(git_dir)

        try:
            f = open(os.path.join(git_dir, 'foo.txt'), 'w')
            f.write('blah')
        except IOError:
            assert False
        finally:
            f.close()
        cwd = os.getcwd()
        os.chdir(git_dir)
        git.add('foo.txt')
        if os.environ.get('TRAVIS_CI') == 'true':
            git.config('--global', 'user.email',
                       '"auto-version-test@travis.ci"')
            git.config('--global', 'user.name',
                       '"Testing on Travis CI"')
        git.commit('-m "Added foo.txt"')
        os.chdir(cwd)

        # Fake Template Path
        mock_working_dir.return_value = tempfile.gettempdir()

        # Now attempt to clone but patch for Exception throw
        self.config.template = 'git+' + git_dir
        self.config._tpl = git_dir
        t = Template(self.config)
        t.copy_template()

        # Clean up
        rmtree(t.project_root)

        self.assertFalse(os.path.isdir(t.config.template))
        self.assertFalse(self.config.cli_opts.error.called)

    @patch('sh.git.clone', side_effect=Exception)
    def test_error_on_clone_exception(self, mock_repo_init):
        self.config.template = 'git+this/wont/work'
        try:
            Template(self.config)
        except:
            assert True
        else:
            assert False

    @patch('os.path.isdir', return_value=False)
    @patch('facio.config.Config._error')
    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_copy_template_failes_if_dir_does_not_exist(
            self, mock_working_dir, mock_error, mock_isdir):
        mock_working_dir.return_value = tempfile.gettempdir()
        tmp_dir = tempfile.mkdtemp(suffix=self.config.project_name, prefix='')
        tmp_dir_name = list(os.path.split(tmp_dir))[-1:][0]
        self.config.project_name = tmp_dir_name
        t = Template(self.config)
        t.copy_template()
        self.config._error.assert_called_with(
            'Unable to copy template, directory does not exist')

    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_excluded_dirs_are_not_copied(self, mock_working_dir):
        mock_working_dir.return_value = tempfile.gettempdir()
        t = Template(self.config)
        t.exclude_dirs.append('.exclude_this')
        t.copy_template()
        self.assertFalse(os.path.isdir(os.path.join(t.project_root,
                                                    '.exclude_this')))
        rmtree(t.project_root)

    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_copy_directory_tree_if_is_dir(self, mock_working_dir):
        mock_working_dir.return_value = tempfile.gettempdir()
        t = Template(self.config)
        t.exclude_dirs.append('.exclude_this')
        t.copy_template()
        self.assertTrue(os.path.isdir(os.path.join(t.project_root,
                                                   'should_copy_this')))
        rmtree(t.project_root)

    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_directory_not_renamed_if_not_in_placeholders(self,
                                                          mock_working_dir):
        mock_working_dir.return_value = tempfile.gettempdir()
        t = Template(self.config)
        t.copy_template()
        self.assertTrue(os.path.isdir(os.path.join(t.project_root,
                                                   '__NOT_IN_PLACEHOLDERS__')))
        rmtree(t.project_root)

    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_rename_files_in_placeholders(self, mock_working_dir):
        mock_working_dir.return_value = tempfile.gettempdir()
        t = Template(self.config)
        t.copy_template()
        self.assertTrue(os.path.isfile(os.path.join(
            t.project_root, '__NOT_IN_PLACEHOLDERS__',
            '%s.txt' % self.config.project_name)))
        rmtree(t.project_root)
