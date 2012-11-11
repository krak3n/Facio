import os
import unittest
import uuid

from mock import MagicMock
from skeletor.template import Template


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

    def ensure_project_cannot_be_created_if_already_exists(self):
        try:
            Template(self.config)
        except Exception:
            assert True
        else:
            assert False
