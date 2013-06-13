"""
.. module:: tests.test_pipeline
   :synopsis: Tests for the facio pipeline module.
"""

import os
import uuid

from mock import MagicMock, patch
from six import StringIO

from .base import BaseTestCase


class PipelineTest(BaseTestCase):
    """ Pipeline Tests """

    def setUp(self):
        # Mock out the config class
        self.config = MagicMock(name='config')
        self.config.project_name = uuid.uuid4().hex  # Random project name
        self.config.django_secret_key = 'xxx'
        self.config.template_settings_dir = 'settings'
        self.config.cli_opts.error = MagicMock(side_effect=Exception)
        self.config.template = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'files', 'template')
        self.config._tpl = self.config.template
        self.puts_patch = patch('facio.template.puts',
                                stream=StringIO)
        self.puts_patch.start()
