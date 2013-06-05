"""
.. module:: tests.test_vcs.git
   :synopsis: Unit tests for the git vcs module
"""

import os
import tempfile
import uuid

from facio.template import Template
from mock import MagicMock, PropertyMock, patch
from sh import git
from six import StringIO
from shutil import rmtree

from ..base import BaseTestCase


class GitTests(BaseTestCase):
    """ Git Tests """

    def setUp(self):
        self.config = MagicMock(name='config')
        self.config.project_name = uuid.uuid4().hex  # Random project name
        self.config.django_secret_key = 'xxx'
        self.config.template_settings_dir = 'settings'
        self.config.cli_opts.error = MagicMock(side_effect=Exception)
        self.puts_patch = patch(
            'facio.template.puts',
            stream=StringIO)
        self.puts_patch.start()
        self.puts_patch_vcs = patch(
            'facio.vcs.git.puts',
            stream=StringIO)
        self.puts_patch_vcs.start()

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
