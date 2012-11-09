from mock import MagicMock
from skeletor.template import Template

from .base import BaseTestCase


class TemplateTests(BaseTestCase):
    """ Template Tests """

    def should_handle_malformed_variables_gracefully(self):
        config = MagicMock(name='config')
        config.variables = 'xy,y'  # Malformed custom variables
        config.project_name = 'test_project'
        t = Template(config)
        self.assertEquals(len(t.place_holders), 6)
