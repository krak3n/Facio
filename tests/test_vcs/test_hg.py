"""
.. module:: tests.test_vcs.hg
   :synopsis: Unit tests for the hg vcs module
"""

import os
import tempfile
import uuid

from facio.template import Template
from mock import MagicMock, PropertyMock, patch
from sh import hg
from shutil import rmtree

from .. import BaseTestCase


class HgTests(BaseTestCase):
    """ Mercurial Tests """

    def setUp(self):
        self.clint_paths = [
            'facio.vcs.hg.puts',
        ]
        self._mock_clint_start()
        self.config = MagicMock(name='config')
        self.config.project_name = uuid.uuid4().hex  # Random project name
        self.config.django_secret_key = 'xxx'
        self.config.template_settings_dir = 'settings'
        self.config.cli_opts.error = MagicMock(side_effect=Exception)

    @patch('sh.Environment.__getitem__', side_effect=ImportError)
    def test_mercurial_import_fails_if_missing(self, mock_sh):
        self.config.template = 'hg+this/wont/work'
        try:
            Template(self.config)
        except ImportError:
            assert True
        else:
            assert False

    @patch('sh.hg.clone', side_effect=Exception)
    def test_error_on_clone_exception(self, mock_repo_init):
        self.config.template = 'hg+this/wont/work'
        try:
            Template(self.config)
        except:
            assert True
        else:
            assert False

    @patch('facio.template.Template.working_dir', new_callable=PropertyMock)
    def test_clone_hg_repo(self, mock_working_dir):
        cwd = os.getcwd()

        if os.environ.get('TRAVIS_CI') == 'true':
            # Set hg users etc
            pass

        # Create a fake temp repo w/ commit
        hg_dir = tempfile.mkdtemp(prefix='hg')
        hg.init(hg_dir)

        try:
            f = open(os.path.join(hg_dir, 'foo.txt'), 'w')
            f.write('blah')
        except IOError:
            assert False
        finally:
            f.close()

        os.chdir(hg_dir)
        hg.add('foo.txt')
        hg.commit('-m "Added foo.txt"')

        os.chdir(cwd)

        # Fake Template Path
        mock_working_dir.return_value = tempfile.gettempdir()

        # Now attempt to clone but patch for Exception throw
        self.config.template = 'hg+' + hg_dir
        self.config._tpl = hg_dir
        t = Template(self.config)
        t.copy_template()

        # Clean up
        rmtree(t.project_root)

        self.assertFalse(os.path.isdir(t.config.template))
        self.assertFalse(self.config.cli_opts.error.called)
