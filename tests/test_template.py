import unittest

from mock import MagicMock
from skeletor.template import Template


class TemplateTests(unittest.TestCase):
    """ Template Tests """

    def setUp(self):
        self.config = MagicMock(name='config')
        self.config.project_name = 'test_project'
        self.config.django_secret_key = 'xxx'
        self.config.template_settings_dir = 'settings'

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
