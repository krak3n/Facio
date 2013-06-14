"""
.. module:: tests.test_pipeline
   :synopsis: Tests for the facio pipeline module.
"""

import os

from facio.pipline import Pipeline
from mock import MagicMock, patch
from six import StringIO

from .base import BaseTestCase


class PipelineTest(BaseTestCase):
    """ Pipeline Tests """

    def setUp(self):
        self.template = self._mock_template_class()
        self.puts = self._mock_puts()

    def _mock_template_class(self):
        template = MagicMock(name='template')
        template.config = MagicMock(name='config')

        return template

    def _mock_puts(self):
        puts = patch('facio.pipeline.puts', stream=StringIO)
        puts.start()

        return puts

    def test_can_parse_file(self):
        self.template.pipeline_file = os.path.join(
            self.test_pieplines_path,
            'complete.yml')
        Pipeline(self.template)
