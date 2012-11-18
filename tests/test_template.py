import os
import tempfile
import unittest
import uuid

from mock import MagicMock, PropertyMock, patch
from skeletor.template import Template
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

    def should_handle_malformed_variables_gracefully(self):
        self.config.variables = 'this,is.wrong'
        t = Template(self.config)

        self.assertEquals(len(t.place_holders), 3)

    def ensure_custom_variables_added_to_placeholders(self):
        self.config.variables = 'foo=bar,baz=1'
        t = Template(self.config)

        self.assertTrue('foo' in t.place_holders)
        self.assertEquals(t.place_holders['foo'], 'bar')
        self.assertTrue('baz' in t.place_holders)
        self.assertEquals(t.place_holders['baz'], '1')

    @patch('skeletor.template.Template.working_dir', new_callable=PropertyMock)
    def ensure_dir_cannot_be_created_if_already_exists(self, mock_working_dir):
        mock_working_dir.return_value = '/tmp/'
        tmp_dir = tempfile.mkdtemp(suffix=self.config.project_name, prefix='')
        tmp_dir_name = list(os.path.split(tmp_dir))[-1:][0]
        self.config.project_name = tmp_dir_name
        try:
            t = Template(self.config)
            t.copy_template()
        except Exception:
            assert True
        else:
            assert False
        os.rmdir(tmp_dir)

    @patch('os.mkdir', return_value=True)
    def ensure_exception_if_directory_creation_fails(self, mock_os_mkdir):
        try:
            t = Template(self.config)
            t.copy_template()
        except Exception:
            assert True
        else:
            assert False
        mock_os_mkdir.assert_called_with(os.path.join(
            t.working_dir, self.config.project_name))

    @patch('sys.stdout', new_callable=StringIO)
    @patch('tempfile.mkdtemp', return_value=True)
    @patch('skeletor.Template.git_clone', return_value=True)
    def should_detect_git_repo(self, mock_git_clone, mock_tempfile,
                               mock_stdout):
        t = Template(self.config)
        assert not t.is_git
        self.config.template = 'git+git@somewhere.com:repo.git'
        t = Template(self.config)
        self.assertEquals('Using git to clone template from '
                          'git@somewhere.com:repo.git\n',
                          mock_stdout.getvalue())
        assert t.is_git
